describe('case_annotation_display_transcripts.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.visit('/');
    cy.get('.analysis-card').first().click();
  });

  it('Displays the transcript in the gene', () => {
    cy.get('[data-test="gene-name"]').click();
    cy.get(':nth-child(1) > .transcript-header > .transcript-header-text').should('exist');
    cy.get(':nth-child(1) > .transcript-header > .transcript-header-text').should('contain', 'NM_001017980.4');
    cy.get(':nth-child(2) > .transcript-header > .transcript-header-text').should('exist');
    cy.get(':nth-child(2) > .transcript-header > .transcript-header-text').should('contain', 'NM_001363810.1');
  });

  it('Displays the transcript in the variant', () => {
    cy.get('[data-test="c-dot"]').click();
    cy.get(':nth-child(1) > .transcript-header > .transcript-header-text').should('exist');
    cy.get(':nth-child(1) > .transcript-header > .transcript-header-text').should('contain', 'NM_001017980.4');
    cy.get(':nth-child(2) > .transcript-header > .transcript-header-text').should('exist');
    cy.get(':nth-child(2) > .transcript-header > .transcript-header-text').should('contain', 'NM_001363810.1');
  });
});
