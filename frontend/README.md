# Rosalution Frontend

Rosalution's frontend is a Vue 3 single page architecture (SPA) application
that provides a visual user experience for interacting with Rosalution
for analysis.

## Setup

### Dependencies

- [Node.JS 16+](https://nodejs.org/en/)
    - Recommended to manageNode.JS versions with [nvm](https://www.npmjs.com/package/npx) - [install](https://github.com/nvm-sh/nvm#install--update-script)
- [Yarn - Classic](https://classic.yarnpkg.com/en/docs/getting-started) - [install](https://classic.yarnpkg.com/en/docs/install#windows-stable)

### Requirements

Rosalution frontend application and development dependencies are managed within
the project's `package.json` in this project directory. Run the following to
setup application and development dependencies using Yarn.

```bash
yarn install
```

## Deployment

Rosalution's frontend currently expects the host address route to end with
`/rosalution/` and for Rosalution's backend service to be available within the same
base URL ending with `/rosalution/api`. Login to the application will **fail** if Rosalution's backend
service is inaccessible.

Use *docker* and *docker compose* facilitate these two dependencies to deploy Rosalution in
it's entirety for local development. Visit [Rosalution's Environment Setup and Deployment](../README.md#environment-setup)
for instructions on how to get started.

The local development deployment of Rosalution uses [Vite](https://vitejs.dev/guide/) to build
and package Rosalution which includes [Hot Module Replacement](https://vitejs.dev/guide/features.html#hot-module-replacement)
in support of rapid development.

## Build

Builds Rosalution frontend for production.

```bash
yarn build
```

## Testing

Rosalution frontend uses [Vitest](https://vitest.dev/), a Vite-native unit test
framework along with:

- [Vue Test Utils](https://test-utils.vuejs.org/) for testing Vue 3 framework
- [Sinon.js](https://sinonjs.org/) for test spies, stubs, and mocking
- [Chai Assertion Library](https://www.chaijs.com/) for assertions, builtin to Vitest

### Unit Tests

Unit testing with Vitest supports hot module reloading by watching for changes
in the project directory. Configuration for unit testing is managed in the
`vite.config.js` in the project directory.

```bash

# Running Unit Testing - Basic
yarn test:unit

# Running Unit Testing - with Watch and Hot Module Reloading
yarn test:unit:watch

# Running Unit Testing - Code Coverage

yarn test:coverage
```

#### Code Coverage

Code coverage configuration is managed in the `vite.config.js` and is generated
by [c8](https://github.com/bcoe/c8#readme).

Visit
`<{root_project_path/rosalution/frontend/coverage/index.html}>` within the browser
to see an HTML report of the code coverage generated from unit tests.

## Static Analysis

Analyze and linting the JavaScript codebase is done via [ESlint](https://eslint.org/).
Rosalution uses the ESLint shareable config for Google's JavaScript style guide
[ESLint Google Config](https://github.com/google/eslint-config-google).

```bash
# Linting
yarn lint

# Auto-Fix Linting
yarn lint:auto
```
