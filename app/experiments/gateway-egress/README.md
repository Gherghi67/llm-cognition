# Gateway egress experiment

This is the disposable verification runner for blocking connections from a compromised
Layer Atlas gateway to other services on the Mac. It builds from the production
files in `app/gateway/`. Running these checks does not change or deploy
`app/compose.yaml`, the live images, the live database, Tailscale, or the Mac firewall.

The runner creates project `layer-atlas-egress-verify`, publishes only
`127.0.0.1:18786`, and uses its own database volume. It refuses to prepare over an
existing verification stack or an occupied test port. Builds have separate image
tags. Generated Compose files and detailed evidence live in the ignored directory
`.cs/local/gateway-egress-verify/`.

The gateway applies an atomic batch to its own `inet atlas_egress` nftables table
before starting Nginx. Other tables, including Docker DNS NAT, remain intact.
New outbound traffic is restricted to the reserved backend IPv4 address on TCP
8786, Docker DNS at `127.0.0.11:53`, local HTTP health checks, and IPv6 neighbor
discovery. Replies to established incoming connections are allowed. Remaining
IPv4 and IPv6 output is rejected.

The output filter uses priority -110, after connection tracking and before
Docker's DNS destination NAT at -100. The actual Docker NAT rules were inspected
and DNS resolution was tested. Priority ordering follows the
[nftables reference](https://www.netfilter.org/projects/nftables/manpage.html).

Docker allocates a fresh internal network from its address pools. The runner
reserves its `.2` IPv4 address for the backend and supplies that same address to
the gateway rule. Backend recreation therefore retains the allowlisted address.
The experiment does not hard-code a subnet or permit a whole subnet. The test network is created through `manage.prepare_network`, owned by its test
project, and removed by the runner. Live maintenance uses the same preparation
code and retains its network across container recreation.

Bootstrap has only `NET_ADMIN`, `SETUID`, `SETGID`, and `SETPCAP` capabilities.
`setpriv` changes to UID/GID 101, clears groups and all capability sets, and enables
no-new-privileges. An additional script checks the actual kernel state before
executing Nginx or a health check. This check is necessary: in the measured Alpine
image, `setpriv` returned success with a nonzero bounding set when `SETPCAP` was
missing. The guarded version refuses to serve in that state. See the
[setpriv reference](https://man7.org/linux/man-pages/man1/setpriv.1.html) for the
requested privilege changes.

`init` is disabled for the gateway so a root init process does not remain. Nginx
is PID 1 and reaps its workers. Docker configuration still specifies root for
bootstrap, and each Docker health check briefly starts the immutable privilege
drop wrapper as root; its HTTP command runs only after the guard succeeds. An
owner-issued `docker exec` still defaults to bootstrap privileges. The tested
security boundary is the Nginx process and its descendants, not a Docker owner.

Docker initially owns the stdout/stderr pipes as root. Bootstrap makes only those
two pipe descriptors writable by the final UID before dropping privileges; this
allows the existing Nginx log configuration to reopen them without extra
capabilities or a writable root filesystem.

To repeat from the repository root with Docker host access, run these actions in
order. The loop stops on failure and leaves the test stack available for inspection.

```sh
for action in prepare build baseline protected acceptance lifecycle failures cleanup; do
    PYTHONDONTWRITEBYTECODE=1 python3 app/experiments/gateway-egress/verify.py "$action" || break
done
```

`cleanup` removes only the disposable containers, networks, and database volume.
It verifies the live container IDs, image IDs, and start times are unchanged and
checks live HTTP health. Test image tags/build cache and ignored evidence remain
available locally. No image pruning is performed.

Measured on 16 November 2026 with Docker Engine 29.9.3, LinuxKit 7.0.14,
nftables 1.1.6-r1, and setpriv 2.42.3-r1:

| Check | Result |
| --- | --- |
| Unprotected connection probes | 23 of 47 succeeded; all five known Mac ports succeeded by hostname, numeric host address, and IPv4-mapped IPv6 |
| Protected connection probes | 0 of 47 succeeded; both IPv4 and IPv6 rejection counters increased |
| Known Mac ports | 9222, 3306, 6379, 8765, 63342; TCP handshakes only |
| Additional paths | Docker gateway/bridge, Mac LAN and Tailscale addresses; controlled reachable IPv4 and IPv6 listeners |
| Runtime privileges | Nginx master and worker UID/GID 101; every capability set zero; no-new-privileges enabled |
| Runtime isolation | Read-only filesystem, bounded tmpfs/resources, no host or Docker socket mounts; backend remains internal |
| DNS and HTTP | Docker DNS and app requests succeed with the filter before DNS NAT |
| Existing app acceptance | Import, notes, tasks, exports, identity forwarding, Host/Origin checks, activity history, backup and restore pass |
| Lifecycle | Backend recreation retains address; gateway restart and recreation retain blocking and app health |
| Failed startup | Missing NET_ADMIN, missing SETPCAP, missing backend address, and invalid backend address all exit without listening |

The runner executes the container acceptance test with its disposable project
and generated Compose path supplied through explicit test settings. The test
asserts project/volume ownership and actual Nginx privileges before mutations.
Eight Python HTTP tests, six network-management tests, and the original Node
numerical fixtures cover the surrounding application and address lifecycle.

This closes the tested post-compromise TCP connection paths. Docker DNS queries
remain allowed, including Docker's forwarding behavior, so this is not a claim
of complete outbound data isolation. It is not a container/VM escape test or a
full Mac reboot test, and it does not establish that a gateway exploit exists.
The original prototype files in this directory are retained as the design record;
the runner now copies and tests the production files from `app/gateway/`. See
`app/README.md` for deployment and maintenance commands.
