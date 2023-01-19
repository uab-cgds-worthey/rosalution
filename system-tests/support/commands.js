// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
Cypress.Commands.add('resetDatabase', () => {
  return cy.exec(`docker-compose exec -T rosalution-db mongosh /tmp/fixtures/seed.js`);
});

Cypress.Commands.add('login', (username) => {
  cy.request({
    method: 'POST',
    url: '/api/auth/loginDev',
    form: true,
    body: {
      username: username,
      password: 'secret',
    },
  });

  cy.getCookie('rosalution_TOKEN').should('exist');
});
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })
