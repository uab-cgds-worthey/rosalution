describe('edit_case_analysis.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.intercept('/rosalution/api/analysis/CPAM0002').as('analysisLoad');
    cy.visit('analysis/CPAM0002');
    cy.wait('@analysisLoad');
  });

  it('edits a value & saves to the analysis', () => {
    
    cy.get('[data-test="user-menu"]')
        .find('.grey-rounded-menu')
        .as('userActionMenu')
        .invoke('attr', 'style', 'display: block; visibility: visible; opacity: 1;');
    cy.get('@userActionMenu').contains('Edit').click();
    cy.get('@userActionMenu').invoke('attr', 'style', 'display: block; visibility: hidden; opacity: 0;');

    cy.get('[href="#Brief"]').click();
    cy.get('#Brief > div > [data-test="Phenotype"] > .section-content > [data-test="editable-value"]')
        .as('editablePhenotype')
        .click();
    cy.get('@editablePhenotype').type('test');
    cy.get('@editablePhenotype').should('contain', 'test');
    
    // Save the changes to persist the analysis
    cy.get('[data-test="save-edit-button"]').should('exist');
    cy.get('[data-test="save-edit-button"]').click();
    cy.get('[data-test="save-edit-button"]').should('not.exist');

    // Verify that the changes persist once the save is complete
    cy.get('[href="#Brief"]').click();
    cy.get('#Brief > div > [data-test="Phenotype"] > .section-content').as('phenotypeField').should('contain', 'test');
    
    // Visit CPAM0046 analysis to verify the updated field in CPAM0002 does not appear
    cy.visit('analysis/CPAM0046');
    cy.wait('@analysisLoad');
    cy.get('[href="#Brief"]').click();
    cy.get('@phenotypeField').contains('test').should('not.exist');

    // Return to CPAM0002 analysis and verify the updated field is persisted
    cy.visit('analysis/CPAM0002');
    cy.wait('@analysisLoad');
    cy.get('[href="#Brief"]').click();
    cy.get('@phenotypeField').contains('test').should('exist');
  });
});
