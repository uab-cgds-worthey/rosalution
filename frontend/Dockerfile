# Local development stage
FROM node:20.8-alpine3.18 AS development-stage
WORKDIR /app
COPY package.json /app/
COPY yarn.lock /app/
COPY index.html /app/
COPY vite.config.js /app/
RUN yarn install
EXPOSE 3000
ENTRYPOINT ["yarn", "dev:host"]

# Production Build stage
FROM node:20.8-alpine3.18 AS production-build
WORKDIR /app
COPY ./src /app/src/
COPY package.json /app/
COPY yarn.lock /app/
COPY index.html /app/
COPY vite.config.js /app/
ARG VERSION_BUILD_TAG=latest

ENV VITE_ROSALUTION_VERSION=$VERSION_BUILD_TAG

RUN yarn install --frozen-lockfile && yarn build --bASe=/rosalution/

FROM nginx:1.25.2-alpine3.18 AS production-stage

COPY etc/default.conf /etc/nginx/conf.d/
COPY --from=production-build /app/dist/ /usr/share/nginx/html/
EXPOSE 80