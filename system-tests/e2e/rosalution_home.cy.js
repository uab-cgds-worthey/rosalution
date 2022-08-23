describe('Rosalution home', () => {
  before(() => {
    cy.resetDatabase();
  });

  it('renders the available analyses as cards', () => {
    cy.visit('/');
    cy.get('.analysis-card').should('have.length', 5);
  });
});
