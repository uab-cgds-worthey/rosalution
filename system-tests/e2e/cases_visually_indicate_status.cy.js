describe('visually_indicate_status.cy.js', () => {
  it('visually indicates status', () => {
    cy.visit('/login');
    cy.get('[data-test="username-input"]').type('user01');
    cy.get('[data-test="local-login-button"]').click();
    cy.get('[href="/rosalution/analysis/CPAM0002"] > .analysis-card > .analysis-base > .case-status-section >' +
    ' .status-icon > .svg-inline--fa').should('have.class', 'fa-check');
    cy.get('[href="/rosalution/analysis/CPAM0047"] > .analysis-card > .analysis-base > .case-status-section >' +
    ' .status-icon > .svg-inline--fa').should('have.class', 'fa-x');
    cy.get('[href="/rosalution/analysis/CPAM0053"] > .analysis-card > .analysis-base > .case-status-section >' +
    ' .status-icon > .svg-inline--fa').should('have.class', 'fa-clipboard-check');
  });

  it('does not visually indicate the wrong status', () => {
    cy.get('[href="/rosalution/analysis/CPAM0002"] > .analysis-card > .analysis-base > .case-status-section >' +
    ' .status-icon > .svg-inline--fa').should('not.have.class', 'fa-x');
    cy.get('[href="/rosalution/analysis/CPAM0047"] > .analysis-card > .analysis-base > .case-status-section >' +
    ' .status-icon > .svg-inline--fa').should('not.have.class', 'fa-check');
    cy.get('[href="/rosalution/analysis/CPAM0053"] > .analysis-card > .analysis-base > .case-status-section >' +
    ' .status-icon > .svg-inline--fa').should('not.have.class', 'fa-asterisk');
  });
});
