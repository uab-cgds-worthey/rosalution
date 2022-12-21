<!-- Add a header image here -->

<!-- CI/CD and other badges here -->

# Rosalution

![license-badge](https://badgen.net/badge/license/GPLv3/blue)

Rosalution: C-PAM Software Tool

---

## Table of Contents

- [introduction](#introduction)
- [License](#license)
- [Installation for Use](#installation-for-use)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Installation for Development](#installation-for-development)
    - [Project Setup](#project-setup)
    - [Local Development](#local-development)
    - [Database, Fixtures, and Seeding the Database](#database-fixtures-and-seeding-the-database)
- [Contributing](#contributing)
    - [Contributing Guidelines](#contributing-guidelines)
    - [Code of Conduct](#code-of-conduct)
    - [How to Report a Bug](#how-to-report-a-bug)
- [API Docs](#api-docs)
- [Maintainers](#maintainers)
- [How to Cite](#how-to-cite)
- [Credits and Acknowledgements](#credits-and-acknowledgements)

---

## Introduction

Rosalution assists researchers study 🧬 variation in patients 🧑🏾‍🤝‍🧑🏼 by helping select candidate animal models 🐀🐁🐠🪱
 to replicate the variation to further research to derive, diagnose, and provide therapies for ultra-rare diseases.

---

## License

Rosalution is licensed under the
 [GNU General Public License v3.0](https://github.com/uab-cgds-worthey/rosalution/blob/main/COPYING).

---

## Installation for Use

- [Prerequisites](#prerequisites)
- [Installation](#installation)

### Prerequisites

- lorem ipsum

### Installation

- lorem ipsum

---

## Installation for Development

- [Project Setup](#project-setup)
- [Local Development](#local-development)
- [Database, Fixtures, and Seeding the Database](#database-fixtures-and-seeding-the-database)
    - [Seeding the Database](#seeding-the-database)
    - [Viewing the Database](#viewing-the-database)

### Project Setup

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

### Local Development

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

### Database, Fixtures, and Seeding the Database

- [Seeding the Database](#seeding-the-database)
- [Viewing the Database](#viewing-the-database)

Fixtures are located in the `<project-root>/etc/fixtures` directory.  Mount
`initial-db-seed.sh` and `./etc/fixtures` with the MongoDB container
respectively to `/docker-entrypoint-initdb.d/initial-db-seed.sh` and
`./tmp/fixtures`.

#### Seeding the Database

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

#### Viewing the Database

Use the following command to view the database within the mongodb container.

```bash
docker exec -it rosalution_rosalution-db_1 mongosh rosalution_db
```

---

## Contributing

- [Contributing Guidelines](#contributing-guidelines)
- [Code of Conduct](#code-of-conduct)
- [How to Report a Bug](#how-to-report-a-bug)

### Contributing Guidelines

We welcome contributions from the community! Please read our [contributing guidelines](url to contributing guidelines)
 to learn how you can help improve the project.

### Code of Conduct

We expect all contributors to adhere to our [code of conduct](url to code of conduct). Please read it before
 contributing to the project.

### How to Report a Bug

If you encounter a bug while using the project, we want to hear about it! Here's how to report a bug:

  1. Check the [existing issues](https://github.com/uab-cgds-worthey/rosalution/issues) to see if the bug has already
   been reported.
  2. If the bug has not already been reported, create a new issue by clicking the "New Issue" button on the
   [issues page](https://github.com/uab-cgds-worthey/rosalution/issues).
  3. In the issue template, provide a clear and concise description of the bug, including any error messages that you
   encountered and steps to reproduce the bug.
  4. If possible, include any relevant details such as the version of the project you are using, your operating system,
   and any other relevant information that may help to reproduce and fix the bug.

We will review your issue and work to resolve the bug as soon as possible. Thank you for helping to improve the project!

---

## API Docs

---

## Maintainers

---

## How to Cite

---

## Credits and Acknowledgements
