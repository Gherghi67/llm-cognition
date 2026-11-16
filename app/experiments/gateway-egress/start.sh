#!/bin/sh
set -eu

# Only a literal supplied by the disposable stack runner can enter the ruleset.
: "${ATLAS_IPV4:?The reserved backend IPv4 address is required}"
case "$ATLAS_IPV4" in
    *[!0-9.]*|'') echo 'Invalid backend IPv4 address' >&2; exit 1 ;;
esac

# The whole batch is atomic and touches only our table. Conntrack runs at -200;
# Docker's embedded-DNS DNAT runs at -100, after this -110 output filter.
/usr/sbin/nft -f - <<EOF
add table inet atlas_egress
flush table inet atlas_egress
table inet atlas_egress {
    chain output {
        type filter hook output priority -110; policy drop;
        ct state invalid counter drop
        ct state established ct direction reply counter accept
        ip daddr $ATLAS_IPV4 tcp dport 8786 counter accept
        ip daddr 127.0.0.11 udp dport 53 counter accept
        ip daddr 127.0.0.11 tcp dport 53 counter accept
        ip daddr 127.0.0.1 tcp dport 8786 counter accept
        ip6 hoplimit 255 icmpv6 type { nd-neighbor-solicit, nd-neighbor-advert } counter accept
        meta nfproto ipv4 counter reject with icmpx type admin-prohibited
        meta nfproto ipv6 counter reject with icmpx type admin-prohibited
    }
}
EOF

# Docker creates these pipe descriptors as root when bootstrap starts as root.
# Permit the final UID to reopen them for Nginx logging, without granting read
# access or adding CHOWN/FOWNER capabilities. Only this container's pipes change.
chmod 0622 /proc/self/fd/1 /proc/self/fd/2

# No root init process remains: Nginx becomes PID 1 and reaps its own workers.
exec /usr/local/bin/unprivileged.sh /usr/sbin/nginx -g 'daemon off;'
