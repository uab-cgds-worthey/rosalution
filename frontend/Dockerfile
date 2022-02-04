# Local development stage
FROM node:17-alpine3.14 as development-stage
WORKDIR /app
RUN yarn install
EXPOSE 3000
ENTRYPOINT ["yarn", "dev:host" ]

# Production Build stage
FROM node:17-alpine3.14 as production-build
WORKDIR /app
COPY ./src /app/src/
COPY package.json /app/
COPY yarn.lock /app/
COPY index.html /app/
COPY vite.config.js /app/

RUN yarn install --frozen-lockfile && yarn build

FROM nginx:1.21.6-alpine as production-stage

COPY --from=production-build /app/dist/ /usr/share/nginx/html/