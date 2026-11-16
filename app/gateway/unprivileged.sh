#!/bin/sh
set -eu
exec /bin/setpriv \
    --reuid=101 --regid=101 --clear-groups \
    --bounding-set=-all --inh-caps=-all --ambient-caps=-all \
    --no-new-privs /usr/local/bin/verify-unprivileged.sh "$@"
