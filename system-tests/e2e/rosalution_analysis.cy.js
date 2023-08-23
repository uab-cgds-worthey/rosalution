describe('As a Clinical Analyst using Rosalution for analysis', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.intercept('/rosalution/api/analysis/CPAM0002').as('analysisLoad');
    cy.visit('/');
    cy.get('.analysis-card')
        .find(':contains(CPAM0002)')
        .find('.case-name').click();
  });

  it.skip('should allow the user to navigate the analysis via the logo, header, and section anchor links', () => {

    const anchorLinks = [
      'Brief', 'Clinical History', 'Pedigree', 'Supporting Evidence', 'VMA21_Gene%20To%20Phenotype',
      'VMA21_Molecular%20Mechanism', 'VMA21_Function', 'Model_Goals',
    ];
    const expectedHeaderLinks =
      ['CPAM0002', 'LOGIN', ...anchorLinks];

    cy.wait('@analysisLoad');
    cy.get('[data-test="primary-content"] > div > a')
      .each(($el) => {
      cy.wrap($el).invoke('text').should('be.oneOf', expectedHeaderLinks).then((text) => {
        if (anchorLinks.includes(text)) {
          const anchorLink = `#${text.replace(' ', '_')}`;
          cy.wrap($el).click().url().should('contain', `analysis/CPAM0002${anchorLink}`);
          cy.get(anchorLink);
        }
      });
    });

    cy.get('[data-test="header-title-text"]').click();
    cy.window().its('scrollY').should('equal', 0);

    cy.get('.rosalution-logo').click();
    cy.url().should('eq', Cypress.config().baseUrl + '/');
  });

  it('should allow the user to navigate to a third party link after adding one', () => {
    
    cy.get('.grey-rounded-menu').invoke('attr', 'style', 'display: block; visibility: visible; opacity: 1;');
    cy.get('[data-test="user-menu"] > .grey-rounded-menu').contains('Attach Monday.com').click();
    cy.get('.grey-rounded-menu').invoke('attr', 'style', 'display: block; visibility: hidden; opacity: 0;');

    cy.get('[data-test="link-input"]').type('https://www.monday.com');
    cy.get('[data-test="confirm"]').click();
    cy.get('[data-test="third-party-link"]').should('exist');
    cy.get('[data-test="third-party-link"]').should('have.attr', 'href', 'https://www.monday.com');
    cy.get('[data-test="third-party-link"]').should('have.attr', 'target', '_blank');
    cy.get('[data-test="third-party-link"]').should('have.attr', 'rel', 'noopener noreferrer');
  });

  it('should update the status icon when the user changes the status', () => {
    cy.visit('/analysis/CPAM0084');

    cy.get('[data-test="status-icon"] > svg').should('have.class', 'fa-asterisk');

    cy.get('.grey-rounded-menu').invoke('attr', 'style', 'display: block; visibility: visible; opacity: 1;');
    cy.get('[data-test="user-menu"] > .grey-rounded-menu > :nth-child(2)').contains('Mark Ready').click();
    cy.get('.grey-rounded-menu').invoke('attr', 'style', 'display: block; visibility: hidden; opacity: 0;');
    
    cy.get('[data-test="status-icon"] > svg').should('have.class', 'fa-clipboard-check');
  });
});
