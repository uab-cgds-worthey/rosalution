describe('import_new_case.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.visit('/');
  });

  it('imports a new analysis', () => {
    cy.get('[data-test="create-card"]').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/new-analysis-import.json', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();
    cy.get('[data-test="notification-dialog-header"]')
      .should('be.visible')
      .and('contain', 'Successful import');
    cy.get('[data-test="confirm-button"]').click();
    cy.get('[data-test="notification-dialog-header"]').should('not.exist');
    cy.visit('/');
    cy.get('app-content').should('contain', 'CPAM0112');
  });

  it('imports a new analysis with a duplicate case ID', () => {
    cy.get('[data-test="create-card"]').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/new-analysis-import.json', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();
    cy.get('[data-test="notification-dialog-header"]')
      .should('be.visible')
      .and('contain', 'Successful import');
    cy.get('[data-test="confirm-button"]').click();
    cy.get('[data-test="notification-dialog"]').should('not.exist');

    cy.visit('/');
    cy.get('app-content').should('contain', 'CPAM0112');
    cy.get('[data-test="create-card"]').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/new-analysis-import.json', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();
    cy.get('[data-test="notification-dialog"]')
      .should('be.visible')
      .and('contain', 'Failed to import analysis')
      .and('contain', 'Error: Status Code: 409 Conflict');
    cy.get('[data-test="confirm-button"]').click();
    cy.get('[data-test="notification-dialog"]').should('not.exist');
  });

  it('tries to import a new case with a file that isn\'t a JSON file', () => {
    cy.get('[data-test="create-card"]').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/example_file_to_upload.txt', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();
    cy.get('[data-test="notification-dialog"]')
      .should('be.visible')
      .and('contain', 'Failed to import analysis')
      .and('contain', 'Error: Status Code: 500 Internal Server Error');
    cy.get('[data-test="confirm-button"]').click();
    cy.get('[data-test="notification-dialog"]').should('not.exist');
  });
});
