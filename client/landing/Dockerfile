FROM node:26 AS builder

WORKDIR /app/client/landing

COPY ./client/landing/package.json ./client/landing/package-lock.json ./

RUN npm install

COPY ./client/landing/ ./

RUN npm run build-only


FROM caddy:2.11

COPY ./client/landing/Caddyfile /etc/caddy/Caddyfile

COPY --from=builder /app/client/landing/dist /usr/landing/
