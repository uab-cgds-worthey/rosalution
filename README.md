# Rosalution

<p align="center">
    <img src="rosalution_title.svg" alt="Rosalution Logo and Title" width="400"/>
</p>

![license-badge](https://badgen.net/badge/license/GPLv3/blue)
![example](https://github.com/uab-cgds-worthey/rosalution/actions/workflows/python.yml/badge.svg)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](code_of_conduct.md)

[Getting Started](#getting-started) • [Testing & Static Analysis](#testing-and-static-analysis) •
[Deployment](#deployment)• [Contributing](#contributing) • [Maintainers](#maintainers) •
[Credits and Acknowledgements](#credits-and-acknowledgements) • [License](#license)

Rosalution assists researchers in studying genetic 🧬 variation in patients 🧑🏾‍🤝‍🧑🏼 by
helping select candidate animal models 🐀🐁🐠🪱 to replicate the variation to
further research to derive, diagnose, and provide therapies for ultra-rare diseases.

Rosalution is the open-source web application maintained and developed by the
[University of Alabama at Birmingham (UAB) Center for Computational Genomics and Data Science (CGDS)](https://sites.uab.edu/cgds/)
to support not only the current [UAB Center for Precision Animal Modeling (C-PAM)](https://sites.uab.edu/cpam/) process,
but also data collection, QA/QC, standardization, integration, dissemination, and collaboration. It also forces and
collects decision points made during the process. The data collected can be mined for process improvement as well as
generation of biological insights. This effort to consolidate both the process and the data is critical; this process
shift is needed to reduce the costs and increase the throughput of precision modeling projects in general.

Rosalution supports three significant aspects of this collaborative animal modeling process.

- ⌨️ configurable case annotation of genes/loci and variants with patient data intake and public 'omics datasets
- ✨ dissemination of data to a large team of interdisciplinary researchers and physicians
- 🌐 collaborative team review and analysis of the case

![First UI screenshot of the Rosalution web application](./docs/figures/rosalution_analysis_ui.png?raw=true "Rosalution Screenshot")

![Second UI screenshot of the Rosalution web application](./docs/figures/rosalution_annotation_ui.png?raw=true "Rosalution Screenshot")

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
- Python environment is not setup with the setup script.  See [Python setup](./backend/README.md#setup) to setup Python environment.

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

## Testing and Static Analysis

- [Unit and Integration Testing](#unit-and-integration-testing)
- [System Testing](#system-testing)
- [Static Analysis](#static-analysis)

### Unit and Integration Testing

Rosalution's entire stack is supported with thorough testing. Refer to the following
on the different testing done within the application.

- [Frontend Testing & Code Coverage](./frontend/README.md#testing)
- [Backend Testing & Code Coverage](./backend/README.md#testing)

It is important to note that your local environment must be setup in order
to run unit testing.

### System Testing

- [Full Stack System Testing](./system-tests/README.md)

System testing requires the entire stack of the application to be successfully
deployed to your local development environment. The environment must be setup
and the application deployed with *docker-compose*. Refer to the following
for a quick start with System Testing done by Cypress.

Our system testing requires that Chrome is available as a browser on the system.
This makes it extremely difficult to setup/run within Windows Subsystem Linux,
so running system testing in WSL2 is not supported.

```bash
# Run System Testing with report displayed in terminal
cd system-tests
yarn test:e2e
```

```bash
# Run System Testing with Cypress UI to visualize and run system testing
cd system-tests
yarn test:e2e:open
```

### Static Analysis

We use linting tools for JavaScript, Python, Docker, Markdown, and Shell scripts for static analysis.
To see the commands and how to run linting,
refer to [Linting and Static Analysis](CONTRIBUTING.md#linting-and-static-analysis) in the [Contributing Guidelines](CONTRIBUTING.md).

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

We welcome contributions from the community! Please read our [Contributing Guidelines](CONTRIBUTING.md)
to learn how you can help improve the project.

### Code of Conduct

We expect all contributors to adhere to our [code of conduct](CODE_OF_CONDUCT.md). Please read it before
 contributing to the project.

### How to Report a Bug

To report a bug, refer to [Reporting Issues](CONTRIBUTING.md#reporting-issues) in the [Contributing Guidelines](CONTRIBUTING.md).

---

## Maintainers

- [Angelina Uno-Antonison](https://github.com/SeriousHorncat)
    - Email: aeunoantonison@uabmc.edu
- [Rabab Fatima](https://github.com/fatimarabab)
- [James Scherer](https://github.com/JmScherer)
- [Alex Moss](https://github.com/kuthedk)

---

## Credits and Acknowledgements

**Elizabeth Worthey, Ph.D.**  
*Principal Investigator*, *Director*,
[Center for Computational Genomics and Data Science (CGDS)](https://sites.uab.edu/cgds/)  
*Co-Director*,
[Center for Precision Animal Modeling - Bioinformatics Section](https://sites.uab.edu/cpam/bis/)  
Heersink School of Medicine, The University of Alabama at Birmingham, Birmingham, AL

**[Center for Computational Genomics and Data Science (CGDS)](https://sites.uab.edu/cgds/)**  
Department of Genetics  
Heersink School of Medicine, The University of Alabama at Birmingham, Birmingham, AL

**[Center for Precision Animal Modeling (C-PAM)](https://sites.uab.edu/cpam/)**  
 The University of Alabama at Birmingham, Birmingham, AL

**Brittany Lasseigne, Ph.D.**  
*Principal Investigator*, *Assistant Professor*, [Lasseigne Lab](https://www.lasseigne.org/)  
Department of Cell, Developmental and Integrative Biology  
*Co-Director*, [Center for Precision Animal Modeling - Bioinformatics Section](https://sites.uab.edu/cpam/bis/)  
Heersink School of Medicine, The University of Alabama at Birmingham, Birmingham, AL

**[Bioinformatics Section(BIS) in the Center for Precision Animal Modeling (C-PAM)](https://sites.uab.edu/cpam/bis)**  
 The University of Alabama at Birmingham, Birmingham, AL

---

## License

Rosalution is licensed under the [GNU General Public License v3.0](COPYING).
