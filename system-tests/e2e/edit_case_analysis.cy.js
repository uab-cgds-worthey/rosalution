describe('edit_case_analysis.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.intercept('/rosalution/api/analysis/CPAM0002').as('analysisLoad');
    cy.visit('analysis/CPAM0002');
    cy.wait('@analysisLoad');
  });

  it('edits a value & saves to the analysis', () => {
    cy.get('.grey-rounded-menu').invoke('attr', 'style', 'display: block; visibility: visible; opacity: 1;');
    cy.get('[data-test="user-menu"] > .grey-rounded-menu > :nth-child(1)').contains('Edit').click();
    cy.get('.grey-rounded-menu').invoke('attr', 'style', 'display: block; visibility: hidden; opacity: 0;');
    cy.get('[href="#Brief"]').click();
    cy.get('#Brief > div > [data-test="Phenotype"] > .section-content > [data-test="editable-value"]')
        .click();
    cy.get('#Brief > div > [data-test="Phenotype"] > .section-content > [data-test="editable-value"]')
        .type('test');
    cy.get('#Brief > div > [data-test="Phenotype"] > .section-content > [data-test="editable-value"]')
        .should('contain', 'test');
    cy.get('[data-test="save-edit-button"]').should('exist');
    cy.get('[data-test="save-edit-button"]').click();
    cy.get('[data-test="save-edit-button"]').should('not.exist');
    cy.get('[href="#Brief"]').click();
    cy.get('#Brief > div > [data-test="Phenotype"] > .section-content > [data-test="value-row"]')
        .should('contain', 'test');
    cy.get('.rosalution-logo').click();
    cy.get('.analysis-card').first().click();
    cy.get('#Brief > div > [data-test="Phenotype"] > .section-content > [data-test="value-row"]')
        .should('contain', 'test');
    cy.get('#Brief > div > [data-test="Nominator"] > .section-content > [data-test="value-row"]')
        .should('contain', 'Dr. Person One');
  });
});
