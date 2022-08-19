describe('Rosalution Analaysis', () => {
  it('allows the user to navigate the analysis page', () => {
    cy.visit('/');
    cy.get('.analysis-card')
        .find(':contains(CPAM0002)')
        .find('.case-name').click();

    const anchorLinks = ['Brief', 'Medical Summary', 'Case Information', 'Supplemental Attachments'];
    const expectedHeaderLinks =
      ['CPAM0002', 'LOGIN', ...anchorLinks];

    cy.get('div.content').get('div > a').each(($el) => {
      cy.wrap($el).invoke('text').should('be.oneOf', expectedHeaderLinks).then((text) => {
        if (anchorLinks.includes(text)) {
          const urlText = text.replace(' ', '%20');
          cy.wrap($el).click().url().should('contain', `analysis/CPAM0002#${urlText}`);
        }
      });
    });
  });
});
