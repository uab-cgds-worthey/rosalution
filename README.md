# Rosalution

<img src="rosalution_title.svg" alt="Rosalution Logo and Title" width="400" style="display: block; margin: 0 auto" />

![license-badge](https://badgen.net/badge/license/GPLv3/blue)
![example](https://github.com/uab-cgds-worthey/rosalution/actions/workflows/python.yml/badge.svg)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](code_of_conduct.md)

Rosalution assists researchers in studying genetic 🧬 variation in patients 🧑🏾‍🤝‍🧑🏼 by
helping select candidate animal models 🐀🐁🐠🪱 to replicate the variation to
further research to derive, diagnose, and provide therapies for ultra-rare diseases.

--- INCLUDE WRITEUP ON ROSALUTION BEING A FULL STACK WEBSITE APPLICATION AND API

[Getting Started](#getting-started) • [Deployment](#deployment) • [Contributing](#contributing)
• [Maintainers](#maintainers) • [How to Cite](#how-to-cite)
• [Credits and Acknowledgements](#credits-and-acknowledgements) • [License](#license)

---

## Getting Started

- [Prerequisites](#prerequisites)
- [Browser Support](#browser-support)
- [Local Development Setup](#local-development-setup)
    - [Clone Repository](#clone-repository)
    - [Environment Setup](#environment-setup)

### Prerequisites

| Node.JS 16 | Python 3.8 | Git        | Docker     | Bash shell |
| ---------- | ---------- | ---------- | ---------- | ---------- |
| 16+        | 3.8        |            |            |            |

### Browser Support

| Chrome | Firefox |
| ------ | ------- |
| 64+    | 86+     |

### Local Development Setup

Clone the Git repository [from GitHub](https://github.com/uab-cgds-worthey/rosalution) locally.

#### Clone Repository

```bash
git clone git@github.com:username/node.git
cd rosalution
```

#### Environment Setup

`setup.sh` provisions your local environment for developing Rosalution.
The script will

- `yarn install` within each subdirectory
- Updates your local `/etc/hosts` to support the local DNS name redirect
'local.rosalution.cgds' to localhost.
- Updates ~/.bashrc file by appending a randomly generated key in `ROSALUTION_KEY`
as an environment variable used for the backend service's auth.
    - Source the `.bashrc` if you are to deploy within the same terminal session.

```bash
./setup.sh
```

**For Windows Subsystem Linux users updating their `/etc/hosts` in WSL2**

> The `/etc/hosts` file must manually update on the Windows side located in
`C:\Windows\System32\drivers\etc` as an administrator.  Then restart the Linux
Subsystem by running the following in Powershell as an administrator

```powershell
Restart-Service LxssManager*
```

---

## Deployment

- [Deploying with Docker-Compose](#deploying-with-docker-compose)
- [Database](#database)
    - [Fixtures](#fixtures)
    - [Seeding the Database](#seeding-the-database)
    - [Interacting with the Databsae](#interacting-with-the-database)

### Deploying With Docker-Compose

Deploy Rosalution from the project's root directory using `docker-compose`.
Be sure that `./setup.sh` has been recently for any recent dependency updates
to be installed in all of the subdirectories.

```bash
# deploy rosalution services within this session
docker-compose up

# deploy services in the background using the `-d` option
docker-compose up --build -d

# force docker images to re-build using the `--build` option
docker-compose up --build
```

### Database

Rosalution uses MongoDB to store the state of the application.

#### Fixtures

MongoDB database fixtures are located in the `<project-root>/etc/fixtures` directory.
The **initial-db-seed.sh** script and **./etc/fixtures/** directory are mounted as
volumes into the database container for use to seed the database.

```yml
rosalution-db:
image: mongo:5.0.9
volumes:
    - ./etc/fixtures/initial-seed/initial-db-seed.sh:/docker-entrypoint-initdb.d/initial-db-seed.sh
    - ./etc/fixtures/:/tmp/fixtures
```

#### Seeding the Database

The MongoDB DB is initially seeded at the time of container startup using the
`/docker-entrypoint-initdb.d/initial-db-seed.sh` script.

> Visit
[MongoDB Initializing a fresh instance](https://hub.docker.com/_/mongo/) for
more information on `/docker-entrypoint-initdb.d` executing scripts at the time
of startup.

When automated testing, Cypress re-seeds the database using the `./etc/fixtures/seed.js` script to
reset Rosalution's state.  The script is executed within the MongoDB database
container with `docker-compose exec`.

```bash
docker-compose exec rosalution-db  mongosh /tmp/fixtures/seed.js
```

#### Interacting with the Database

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

We expect all contributors to adhere to our [code of conduct](CODE_OF_CONDUCT.md). Please read it before
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

## Maintainers

---

## How to Cite

---

## Credits and Acknowledgements

---

## License

Rosalution is licensed under the
 [GNU General Public License v3.0](https://github.com/uab-cgds-worthey/rosalution/blob/main/COPYING).
