describe('Rosalution home', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.intercept('/rosalution/api/analysis/CPAM0002').as('analysisLoad');
  });

  it('renders the available analyses as cards', () => {
    cy.visit('/');
    cy.get('[data-test="analysis-card"]').should('have.length', 7);
  });

  it('should allow the user to navigate to a third party link from the card after adding one', () => {
    cy.visit('analysis/CPAM0002');
    cy.wait('@analysisLoad');

    cy.get('.grey-rounded-menu').invoke('attr', 'style', 'display: block; visibility: visible; opacity: 1;');
    cy.get('[data-test="user-menu"] > .grey-rounded-menu > :nth-child(7)')
        .contains('Attach Monday.com')
        .click({force: true});
    cy.get('.grey-rounded-menu').invoke('attr', 'style', 'display: block; visibility: hidden; opacity: 0;');
    cy.get('[data-test="link-input"]').type('https://www.monday.com');
    cy.get('[data-test="confirm"]').click();

    cy.get('.rosalution-logo').click();
    cy.get('[href="/rosalution/analysis/CPAM0002"]').find('[data-test="linkout-section"]').should('exist');
    cy.get('[data-test="third-party-link"]').should('exist');
    cy.get('[data-test="third-party-link"]').should('have.attr', 'href', 'https://www.monday.com');
    cy.get('[data-test="third-party-link"]').should('have.attr', 'target', '_blank');
    cy.get('[data-test="third-party-link"]').should('have.attr', 'rel', 'noopener noreferrer');
  });
});
