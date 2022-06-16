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

## Production Build and Deployment

Use the the production docker-compose.production.yml to build & deploy Rosalution
for production.

```bash
docker-compose -f docker-compose.production.yml up --build
```
