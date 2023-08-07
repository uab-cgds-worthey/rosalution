describe('case_annotation_visualize_score.cy.js', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it.skip('Displays Blue to represent Nominal, and Yellow to represent potentially relevant', () => {
    cy.get('.analysis-card').first().click();
    cy.get('[data-test="gene-name"]').click();
    cy.get('[data-test="score-background"]').should('exist');
    cy.get('[data-test="score-background"]').should('have.attr', 'style', 'background-color:' +
    ' var(--rosalution-blue-300); border-color: 2px solid var(--rosalution-blue-100);');

    cy.get(':nth-child(1) > .transcript-header > .dataset-container > .highlight-text').should('exist');
    cy.get(':nth-child(1) > .transcript-header > .dataset-container > .highlight-text').should('have.attr', 'style',
        'background-color: var(--rosalution-yellow-200);');
  });

  it('displays Red to represent Relevant', () => {
    cy.get('[href="/rosalution/analysis/CPAM0047"]').click();
    cy.get('[data-test="gene-name"]').click();
    cy.get(':nth-child(1) > .transcript-header > .dataset-container > .highlight-text').should('exist');
    cy.get(':nth-child(1) > .transcript-header > .dataset-container > .highlight-text').should('have.attr', 'style',
        'background-color: var(--rosalution-red-200);');
  });
});
