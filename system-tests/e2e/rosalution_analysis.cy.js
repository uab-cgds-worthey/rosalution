describe('As a Clinical Analyst using Rosalution for analysis', () => {
  beforeEach(() => {
    cy.visit('/');
  });
  it('should allow the user to navigate the analysis via the logo, header, and section anchor links', () => {
    cy.get('.analysis-card')
        .find(':contains(CPAM0002)')
        .find('.case-name').click();

    const anchorLinks = ['Brief', 'Clinical History', 'Pedigree', 'Supporting Evidence'];
    const expectedHeaderLinks =
      ['CPAM0002', 'LOGIN', ...anchorLinks];

    cy.get('div.content').get('div > a').each(($el) => {
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
});
