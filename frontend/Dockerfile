# Local development stage
FROM node:16.2-alpine3.12 as development-stage
WORKDIR /app
COPY package.json /app/
COPY yarn.lock /app/
COPY index.html /app/
COPY vite.config.js /app/
RUN yarn install
EXPOSE 3000
ENTRYPOINT ["yarn", "dev:host"]

# Production Build stage
FROM node:16.2-alpine3.12 as production-build
WORKDIR /app
COPY ./src /app/src/
COPY package.json /app/
COPY yarn.lock /app/
COPY index.html /app/
COPY vite.config.js /app/

RUN yarn install --frozen-lockfile && yarn build --base=/rosalution/ --debug

FROM nginx:1.17.6-alpine as production-stage

COPY etc/default.conf /etc/nginx/conf.d/
COPY --from=production-build /app/dist/ /usr/share/nginx/html/
EXPOSE 80