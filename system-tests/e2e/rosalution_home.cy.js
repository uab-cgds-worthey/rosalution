describe('Rosalution home', () => {
  before(() => {
    cy.resetDatabase();
  });

  it('renders the available analyses as cards', () => {
    cy.visit('/login');
    cy.get('[data-test="username-input"]').type('user01');
    cy.get('[data-test="local-login-button"]').click();
    cy.get('.analysis-card').should('have.length', 5);
  });
});
