FROM node:26 AS builder

WORKDIR /app

COPY ./package.json ./package-lock.json ./

RUN npm install

COPY ./ ./

RUN npm run build-only


FROM nginx:1.31-alpine

COPY ./nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=builder /app/dist /usr/web/
