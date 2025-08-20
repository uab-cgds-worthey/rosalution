# Local development stage
FROM node:23.4-alpine3.21 AS development-stage
WORKDIR /app
COPY package.json /app/
COPY yarn.lock /app/
COPY index.html /app/
COPY public/rosalution.ico /app/public/rosalution/rosalution.ico
COPY vite.config.js /app/
RUN yarn install
EXPOSE 3000
ENTRYPOINT ["yarn", "dev:host"]

# Production Build stage
FROM node:23.4-alpine3.21 AS production-build
WORKDIR /app
COPY ./src /app/src/
COPY package.json /app/
COPY yarn.lock /app/
COPY index.html /app/
COPY vite.config.js /app/
COPY public/rosalution.ico /app/public/rosalution/rosalution.ico
ARG VERSION_BUILD_TAG=latest

ENV VITE_ROSALUTION_VERSION=$VERSION_BUILD_TAG

RUN yarn install --frozen-lockfile && yarn build --base=/rosalution/

FROM nginx:1.26.2-alpine3.20 AS production-stage

COPY etc/default.conf /etc/nginx/conf.d/
COPY --from=production-build /app/dist/ /usr/share/nginx/html/
COPY public/rosalution.ico /usr/share/nginx/html/rosalution/rosalution.ico
EXPOSE 80