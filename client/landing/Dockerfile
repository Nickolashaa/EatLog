FROM node:26 AS builder

WORKDIR /app/client/web

COPY ./client/web/package.json ./client/web/package-lock.json ./

RUN npm install

COPY ./client/web/ ./

RUN npm run build-only


FROM caddy:2.11

COPY ./client/web/Caddyfile /etc/caddy/Caddyfile

COPY --from=builder /app/client/web/dist /usr/web/
