FROM node:26 AS builder

WORKDIR /app/client/web

COPY ./client/web/package.json ./client/web/package-lock.json ./

RUN npm install

COPY ./client/web/ ./

RUN npm run build-only


FROM nginx:1.31-alpine

COPY ./client/web/nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=builder /app/client/web/dist /usr/web/
