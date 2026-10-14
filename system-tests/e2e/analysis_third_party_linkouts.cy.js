describe('As a Clinical Analyst using Rosalution for analysis', () => {
  beforeEach(() => {
    cy.resetDatabase();
  });

  it('should allow the user to access, add, and navigate to third party linkouts', () => {
    cy.visit('analysis/CPAM0002');
    cy.get('.grey-rounded-menu').invoke('attr', 'style', 'display: block; visibility: visible; opacity: 1;');
    cy.get('[data-test="user-menu"] > .grey-rounded-menu').contains('Attach Monday.com').click({force: true});
    cy.get('.grey-rounded-menu').invoke('attr', 'style', 'display: block; visibility: hidden; opacity: 0;');

    cy.get('[data-test="link-input"]').type('https://www.monday.com');
    cy.get('[data-test="confirm"]').click();
    cy.get('[data-test="third-party-link"]')
        .should('be.visible')
        .and('have.attr', 'target', '_blank')
        .and('have.attr', 'rel', 'noopener noreferrer')
        .and('have.attr', 'href', 'https://www.monday.com')
        .find('img')
        .should('be.visible')
        .and('have.prop', 'naturalWidth')
        .should('be.greaterThan', 0);

    cy.visit('analysis/CPAM0046');

    const thirdPartyLinks = [
      'https://www.wrike.com/open.htm?id=4584207732',
      'https://www.wrike.com/open.htm?id=4584206752',
    ];

    cy.get('[data-test="analysis-view-header"]').find('[data-test="third-party-link"]').each(($el) => {
      cy.wrap($el)
          .should('be.visible')
          .and('have.attr', 'target', '_blank')
          .and('have.attr', 'rel', 'noopener noreferrer')
          .invoke('attr', 'href')
          .should('be.oneOf', thirdPartyLinks);

      cy.wrap($el)
          .find('img')
          .should('be.visible')
          .and('have.prop', 'naturalWidth')
          .should('be.greaterThan', 0);
    });
  });
});
