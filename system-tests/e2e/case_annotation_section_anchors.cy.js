describe('case_annotation_display_transcripts.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.visit('/');
    cy.get('.analysis-card').first().click();
    cy.get('[data-test="gene-name"]').click();
  });

  it('navigates to the annotation sections via anchor links', () => {
    const anchorLinks = ['Gene', 'Variant', 'Chromosomal Localization', 'Secondary Structure', 'Casual Variant',
      'Variant Publications', 'Gene Homology', 'Human Gene_Expression', 'Human Gene_versus_Protein_Expression',
      'Expression Profiles', 'Orthology', 'Mouse Model', 'Rat Model', 'Zebrafish Model', 'Worm Model', 'Modelability',
      'Druggability'];
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
