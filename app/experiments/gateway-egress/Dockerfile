FROM nginx:stable-alpine@sha256:901e593c95dc85f5a729f5765516321366ef4ac401821431d408897e95287d0a

RUN apk add --no-cache nftables setpriv
COPY --chmod=644 nginx.conf /etc/nginx/nginx.conf
COPY --chmod=755 start.sh unprivileged.sh verify-unprivileged.sh /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/start.sh"]
