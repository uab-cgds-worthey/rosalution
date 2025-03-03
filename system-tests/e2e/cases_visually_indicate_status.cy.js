describe('visually_indicate_status.cy.js', () => {
  beforeEach(() => {
    cy.visit('/');
  });
  it('visually indicates status', () => {
    cy.get('[href="/rosalution/analysis/CPAM0002"]').find('[data-test="status-icon"]').should('have.class', 'fa-check');
    cy.get('[href="/rosalution/analysis/CPAM0047"]').find('[data-test="status-icon"]').should('have.class', 'fa-x');
    cy.get('[href="/rosalution/analysis/CPAM0053"]')
      .find('[data-test="status-icon"]')
      .should('have.class', 'fa-clipboard-check');
  });

  it('does not visually indicate the wrong status', () => {
    cy.get('[href="/rosalution/analysis/CPAM0002"]').find('[data-test="status-icon"]').should('not.have.class', 'fa-x');
    cy.get('[href="/rosalution/analysis/CPAM0047"]')
      .find('[data-test="status-icon"]')
      .should('not.have.class', 'fa-check');
    cy.get('[href="/rosalution/analysis/CPAM0053"]')
      .find('[data-test="status-icon"]')
      .should('not.have.class', 'fa-asterisk');
  });
});
