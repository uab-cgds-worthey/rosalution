describe('Rosalution home', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.visit('/');
  });

  it('renders the available analyses as cards', () => {
    cy.get('.analysis-card').should('have.length', 6);
  });

  it('should allow the user to navigate to a third party link from the card after adding one', () => {
    cy.get('.analysis-card')
        .find(':contains(CPAM0002)')
        .find('.case-name').click();

    cy.get('.grey-rounded-menu').invoke('attr', 'style', 'display: block; visibility: visible; opacity: 1;');
    cy.get('[data-test="user-menu"] > .grey-rounded-menu > :nth-child(4)').contains('Attach Monday.com').click();
    cy.get('.grey-rounded-menu').invoke('attr', 'style', 'display: block; visibility: hidden; opacity: 0;');
    cy.get('[data-test="link-input"]').type('https://www.monday.com');
    cy.get('[data-test="confirm"]').click();

    cy.get('.rosalution-logo').click();
    cy.get('[href="/rosalution/analysis/CPAM0002"] > .analysis-card > .analysis-base > .logo-links-section')
        .should('exist');
    cy.get('[data-test="third-party-link"]').should('exist');
    cy.get('[data-test="third-party-link"]').should('have.attr', 'href', 'https://www.monday.com');
    cy.get('[data-test="third-party-link"]').should('have.attr', 'target', '_blank');
    cy.get('[data-test="third-party-link"]').should('have.attr', 'rel', 'noopener noreferrer');
  });
});
