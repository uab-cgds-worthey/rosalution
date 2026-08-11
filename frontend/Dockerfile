FROM node:26.5-trixie-slim AS base-stage
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME/bin:$PATH"
WORKDIR /app
COPY . /app
RUN npm install -g pnpm@11.20.0

# Local development stage
FROM base-stage AS development-stage
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile
EXPOSE 3000
ENTRYPOINT ["pnpm", "run", "dev:host"]

# Only production build depedencies install
FROM base-stage AS production-dependencies
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --prod --frozen-lockfile

# Production Build stage
FROM base-stage AS production-build
ARG VERSION_BUILD_TAG=latest
ENV VITE_ROSALUTION_VERSION=$VERSION_BUILD_TAG
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile
RUN pnpm build --base=/rosalution/

FROM nginx:1.31.3-alpine3.24 AS production-stage

COPY etc/default.conf /etc/nginx/conf.d/
COPY --from=production-build /app/dist/ /usr/share/nginx/html/
COPY public/rosalution.ico /usr/share/nginx/html/rosalution/rosalution.ico
EXPOSE 80