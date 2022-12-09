describe('case_annotation_display_transcripts.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.visit('/login');
    cy.get('[data-test="username-input"]').type('user01');
    cy.get('[data-test="local-login-button"]').click();
    cy.get('.analysis-card').first().click();
    cy.get('[data-test="gene-name"]').click();
  });

  it('navigates to the annotation sections via anchor links', () => {
    const anchorLinks = ['Gene', 'Variant', 'Gene Homology', 'Protein Expression', 'Modelability',
      'Model Systems', 'Druggability'];
    const expectedSidebarLinks = [...anchorLinks];

    cy.get('.sidebar').find('a').each(($el) => {
      cy.wrap($el).invoke('text').should('be.oneOf', expectedSidebarLinks).then((text) => {
        if (anchorLinks.includes(text)) {
          const anchorLink = `#${text.replace(' ', '_')}`;
          cy.wrap($el).click().url().should('contain', `analysis/CPAM0002/annotation/${anchorLink}`);
          cy.get(anchorLink);
        }
      });
    });
  });
});
