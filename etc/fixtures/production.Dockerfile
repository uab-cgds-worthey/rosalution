FROM mongo:5.0.9 as production-stage
COPY --chmod=0777 ./initial-seed/initial-db-seed.sh /docker-entrypoint-initdb.d/initial-db-seed.sh
COPY ./initial-seed/ /tmp/fixtures/initial-seed/
