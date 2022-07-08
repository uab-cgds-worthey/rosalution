# System Tests

## Cypress

Fast, easy and reliable testing for anything that runs in a browser.

Our system tests uses Cypress to end to end test the application.

[Cypress](https://www.cypress.io)

[Cypress Docks](https://docs.cypress.io/guides/overview/why-cypress)

## Setup

Before running system tests, you must first install cypress with yarn

This can be accomplished by running the following command in the system-tests folder of this project:

```bash
yarn install
```

## Running system tests

To run the system tests, you need to have rosalution running locally in a docker container.

to run system tests, run the following command:

``` bash
yarn test:e2e
```
