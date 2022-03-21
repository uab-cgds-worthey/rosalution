# diverGen

diverGen: C-PAM Software Tool

## Project Setup

`setup.sh` provisions your local environment for developing diverGen.  The script
executes `yarn install` within each sub directory and updates your local
/etc/hosts to support the local DNS name redirect 'local.divergen.cgds' to
localhost.

```bash
./setup.sh
```

## Local Development

For local development, deploy the application from the project root directory
using docker-compose.  Be sure that `./setup.sh` has been recently for any
recent depdency updates to be installed in all of the subfolders.

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

## Production Build and Deployment

Use the the production docker-compose.production.yml to build & deploy diverGen
for production.

```bash
docker-compose -f docker-compose.production.yml up --build
```
