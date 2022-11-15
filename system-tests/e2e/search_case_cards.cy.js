describe('search_case_cards.cy.js', () => {
  it('searches for cases', () => {
    cy.visit('/login');
    cy.get('[data-test="username-input"]').type('user01');
    cy.get('[data-test="local-login-button"]').click();
    cy.get('[data-test="analysis-search"]').type('c.164G>T');
    cy.get('.analysis-card > .analysis-base').should('contain', 'c.164G>T');
    cy.get('[data-test="analysis-search"]').clear();
    cy.get('[data-test="analysis-search"]').type('CMT4B3 Foundation');
    cy.get('.analysis-card > .analysis-base').should('contain', 'CMT4B3 Foundation');
    cy.get('[data-test="analysis-search"]').clear();
    cy.get('[data-test="analysis-search"]').type('CPAM0053');
    cy.get('.analysis-card > .analysis-base').should('contain', 'CPAM0053');
    cy.get('[data-test="analysis-search"]').clear();
  });
});
