describe('search_case_cards.cy.js', () => {
  beforeEach(() => {
    cy.visit('/');
  });
  it('searches for cases', () => {
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

  it('searches for cases with no results', () => {
    cy.get('[data-test="analysis-search"]').type('asdfasdfasdf');
    cy.get('.analysis-card').should('not.exist');
    cy.get('[data-test="analysis-search"]').clear();
  });

  it('searches for cases with no results and then searches for a case that does exist', () => {
    cy.get('[data-test="analysis-search"]').type('asdfasdfasdf');
    cy.get('.analysis-card').should('not.exist');
    cy.get('[data-test="analysis-search"]').clear();
    cy.get('[data-test="analysis-search"]').type('CPAM0002');
    cy.get('.analysis-card > .analysis-base').should('contain', 'CPAM0002');
    cy.get('[data-test="analysis-search"]').clear();
  });

  it('searches and only finds what it searched for', () => {
    cy.get('[data-test="analysis-search"]').type('CPAM004');
    cy.get('.analysis-card > .analysis-base').should('contain', 'CPAM0047');
    cy.get('.analysis-card > .analysis-base').should('contain', 'CPAM0046');
    cy.get('.analysis-card > .analysis-base').should('not.contain', 'CPAM0002');
    cy.get('.analysis-card').should('have.length', 2);
    cy.get('[data-test="analysis-search"]').clear();
  });
});
