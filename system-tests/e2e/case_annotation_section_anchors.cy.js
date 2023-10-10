describe('case_annotation_display_transcripts.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.visit('/');
    cy.get('.analysis-card').first().click();
    cy.get('[data-test="gene-name"]').click();
  });

  it('navigates to the annotation sections via anchor links', () => {
    const anchorLinks = ['Gene', 'Variant', 'Chromosomal Localization', 'Secondary Structure', 'Causal Variant',
      'Variant Publications', 'Gene Homology', 'Human Gene Expression', 'Human Gene versus Protein Expression',
      'Expression Profiles', 'Orthology', 'Rattus norvegicus Model System', 'Mus musculus Model System',
      'Danio rerio Model System', 'C elegans Model System', 'Modelability', 'Druggability'];
    const expectedSidebarLinks = [...anchorLinks];

    cy.get('.sidebar').find('a').each(($el) => {
      cy.wrap($el).invoke('text').should('be.oneOf', expectedSidebarLinks).then((text) => {
        if (anchorLinks.includes(text)) {
          const anchorLink = `#${text.replace(/ /g, '_')}`;
          cy.wrap($el).click();
          cy.url().should('contain', `analysis/CPAM0002/annotation/${anchorLink}`);
          cy.get(anchorLink);
        }
      });
    });
  });
});
