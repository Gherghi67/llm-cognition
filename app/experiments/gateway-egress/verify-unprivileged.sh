#!/bin/sh
set -eu

# setpriv can return success without clearing CapBnd if SETPCAP is missing.
# Check kernel state before executing either Nginx or a health-check command.
checked=0
while read -r key a b c d; do
    case "$key" in
        Uid:|Gid:)
            if [ "$a $b $c $d" != '101 101 101 101' ]; then
                echo "Unsafe gateway privileges: $key" >&2
                exit 1
            fi
            checked=$((checked + 1))
            ;;
        CapInh:|CapPrm:|CapEff:|CapBnd:|CapAmb:)
            case "$a" in
                *[!0]*|'') echo "Unsafe gateway privileges: $key is not zero" >&2; exit 1 ;;
            esac
            checked=$((checked + 1))
            ;;
        NoNewPrivs:)
            [ "$a" = 1 ] || exit 1
            checked=$((checked + 1))
            ;;
        Groups:)
            [ -z "$a$b$c$d" ] || exit 1
            checked=$((checked + 1))
            ;;
    esac
done < /proc/self/status
[ "$checked" = 9 ] || exit 1
exec "$@"
