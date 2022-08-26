# Rosalution

Rosalution: C-PAM Software Tool

## Project Setup

`setup.sh` provisions your local environment for developing Rosalution.  The script
executes `yarn install` within each sub directory and updates your local
/etc/hosts to support the local DNS name redirect 'local.rosalution.cgds' to
localhost.

```bash
./setup.sh
```

Note for Windows Subsystem Linux users, to update the `/etc/hosts` in WSL2,
you must manually update the file on the Windows side located in
`C:\Windows\System32\drivers\etc` as an administrator and restart the Linux
Subsystem by running the following in Powershell as an administrator
`Restart-Service LxssManager*`.

## Local Development

For local development, deploy the application from the project root directory
using docker-compose.  Be sure that `./setup.sh` has been recently for any
recent dependency updates to be installed in all of the subfolders.

```bash
docker-compose up
```

To to deploy services in the background use the `-d` option

```bash
docker-compose up --build -d
```

To force images to re-build, use the `--build` option

```bash
docker-compose up --build
```

## Database, Fixtures, and Seeding the Database

Fixtures are located in the `<project-root>/etc/fixtures` directory.  Mount
`initial-db-seed.sh` and `./etc/fixtures` with the MongoDB container
respectively to `/docker-entrypoint-initdb.d/initial-db-seed.sh` and
`./tmp/fixtures`.

### Seeding the Database

The database is initially seeded at the time of container startup using the
`/docker-entrypoint-initdb.d/initial-db-seed.sh` script.  See
<https://hub.docker.com/_/mongo/>[MongoDB Initializing a fresh instance] for
more information on `/docker-entrypoint-initdb.d` and how `*.js` and `*.sh`
scripts are executed at the time of startup in that directory.

`./etc/fixtures/seed.js` script is used to reset the state of the database or
update it to be within a different state.  Cypress will utilize this script
via a `docker-compose exec` command to run the script within the mongodb
database container, as seen below.

```bash
docker-compose exec rosalution-db  mongosh /tmp/fixtures/seed.js
```

### Viewing the Database

Use the following command to view the database within the mongodb container.

```bash
docker exec -it rosalution_rosalution-db_1 mongosh rosalution_db
```

## Production Build and Deployment

Use the the production docker-compose.production.yml to build & deploy Rosalution
for production.

```bash
docker-compose -f docker-compose.production.yml up --build
```
