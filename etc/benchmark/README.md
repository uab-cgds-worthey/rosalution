# Benchmarking REST API

Preliminary effort to programatically execute basic benchmarking Rosalution's' performance.

## Prerequisites

- [Node.js 26.3+](https://nodejs.org/en/)
    - Node.js recommends managing Node.js installations with [nvm](https://github.com/nvm-sh/nvm) - [install](https://nodejs.org/en/download)
        - Use following dropdown menu options on the Node.js and nvm install page:  
          *Get Node.js `26.3+` for `<your target os> ex. macOS` using `nvm` with `npm`*
- [Docker 17.12.0+](https://www.docker.com/) with `docker-compose` CLI or `docker compose` from Docker Desktop - [Install](https://www.docker.com/)

## Environment Setup

Store Rosalution API credentials in `secrets.file` in benchmark directory:

    ```secrets.file
    CLIENT_ID=XXXXXXXXXXXXXX
    CLIENT_SECRET=XXXXXXXXXXXX
    ```

## Run Benchmarking

Benchmark use `k6` executed within a Docker container.  Npm scripts defined in `package.json` wrap the docker
run commands for simplicity.

### Benchmarking on Local Machine

Executes the benchmark container on the same local Docker network as Rosalution using the Rosalution API credentials.

`npm run benchmark:local:api tests/<test file>`

ex.

`npm run benchmark:local:api tests/avg-get-projects.js`

### Bencharming on Dev Environment

Executes the benchmark container on the same Docker network on the Dev deployment as Rosalution using the
Rosalution API credentials.

`npm run benchmark:dev:api tests/<test file>`

ex.

`npm run benchmark:dev:api tests/avg-get-projects.js`

## Bundling Benchmark Results

Use the provided `bundleBenchmark.sh` script to collect all benchmark artifcats into a single output directory.
Bencharmking artifacts include the `k6` benchmark test run summary and backend service PyInstrument performance
profile.

### Example: Bundling Local Results

This will move both the Pyinstrument profiling and k6-summary.json benchmark run summary to a new directory within
the current run directory.

    ```bash
    ./bundleBenchmark.sh \
    --pyinstrument "<absolute-path-to-rosalution>/rosalution/backend/profile.speedscope.json" \
    -k6 "<absolute-path-to-rosalution>/rosalution/etc/benchmark/k6-summary.json" \
    --output "<absolute-path-to-rosalution>/rosalution/etc/benchmark/"
    ```

### Example: Bundling Dev Results

This will SSH to target machine and use docker to copy the Pyinstrument profiling to the current host machine, pull
the k6-summary.json benchmark run summary, and save them in a new directory within the current run directory.

    ```bash
    sudo ./bundleBenchmark.sh \
    --remote "-i <private-ssh-key> <ssh-user@ip>" \
    --docker "rosalution-prod_backend.1.sb49011lh3e4az4s71vt9vo1u" \
    --pyinstrument "/app/profile.html" \
    -k6 "/mnt/persistent/opt/rosalution/etc/benchmark/k6-summary.json"
    ```
