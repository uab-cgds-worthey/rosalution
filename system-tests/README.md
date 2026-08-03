# System Tests

## Cypress

Fast, easy and reliable testing for anything that runs in a browser.

Our system tests uses Cypress to end to end test the application.

[Cypress](https://www.cypress.io)

[Cypress Docks](https://docs.cypress.io/guides/overview/why-cypress)

## Setup

Before running system tests, you must first install cypress with pnpm

This can be accomplished by running the following command in the system-tests folder of this project:

```bash
pnpm install
```

## Running system tests

To run the system tests, Rosalution must be running locally in a docker container.

Once Rosalution is running, you can run the system tests by running the following command:

```bash
pnpm run test:e2e
```

To watch the system tests run in your Google Chrome browser, run the following command:

```bash
pnpm run test:e2e:open
```
