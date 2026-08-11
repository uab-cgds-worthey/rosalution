(Cypress.config('isInteractive') ? describe : describe.skip)('import_new_analysis_success.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.intercept('/rosalution/api/analysis/summary').as('summaryLoad');
    cy.visit('/');
    cy.wait('@summaryLoad');
  });

  it('imports a new analysis', () => {
    cy.get('[data-test="create-card"]').click();

    cy.get('.project-select-content').select('CPAM');
    cy.get('.drop-file-box-content').selectFile('fixtures/successful-new-analysis-import.json', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();

    cy.get('[data-test="notification-dialog"]')
        .should('be.visible')
        .and('contain', 'Confirm Analysis Import into Project \'CPAM\'');
    cy.get('[data-test="confirm-button"]').click();

    cy.get('[data-test="notification-dialog"]')
        .should('be.visible')
        .and('contain', 'Successful import');
    cy.get('[data-test="confirm-button"]').click();
    cy.get('[data-test="notification-dialog"]').should('not.exist');
    cy.visit('/');
    cy.get('app-content').should('contain', 'CPAM0112');
  });
});
