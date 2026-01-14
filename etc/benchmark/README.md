# Benchmarking REST API

Preliminary effort to programatically execute basic benchmarking Rosalution's' performance.

## Prerequisites

- [Node.JS 23.4+](https://nodejs.org/en/) & [Classic Yarn](https://classic.yarnpkg.com/en/)
    - Node.JS recommends managing Node.JS installations with [nvm](https://www.npmjs.com/package/npx) - [install](https://github.com/nvm-sh/nvm#install--update-script)
    - Yarn is not included with Node.JS with `nvm`. Run `npm install --global yarn` once Node.JS is installed. - [install](https://classic.yarnpkg.com/en/docs/install)
- [Docker 17.12.0+](https://www.docker.com/) with `docker-compose` CLI or `docker compose` from Docker Desktop - [Install](https://www.docker.com/)

## Environment Setup

- Rosalution API Saved as `secrets.file` in benchmark directory

    ```secrets.file
    CLIENT_ID=XXXXXXXXXXXXXX
    CLIENT_SECRET=XXXXXXXXXXXX
    ```

## Run Benchmarking

k6 is executed within a docker container.  The docker run command is aliased with NPM within package.json.

`npm run benchmark:local:api tests/<test file>`

ex.

`npm run benchmark:local:api tests/avg-get-projects.js`

