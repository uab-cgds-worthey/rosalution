describe('import_new_case.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.visit('/');
  });

  it('imports a new case', () => {
    cy.get('.analysis-create-card').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/phenotips-import.json', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();
    cy.get('h2').should('contain', 'Successful import');
    cy.get('.modal-container').should('exist');
    cy.get('[data-test="confirm-button"]').click();
    cy.get('.modal-container').should('not.exist');
    cy.visit('/');
    cy.get('app-content').should('contain', 'CPAM0112');
  });

  it('imports a new case with a duplicate case ID', () => {
    cy.get('.analysis-create-card').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/phenotips-import.json', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();
    cy.get('h2').should('contain', 'Successful import');
    cy.get('.modal-container').should('exist');
    cy.get('[data-test="confirm-button"]').click();
    cy.get('.modal-container').should('not.exist');
    cy.visit('/');
    cy.get('app-content').should('contain', 'CPAM0112');
    cy.get('.analysis-create-card').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/phenotips-import.json', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();
    cy.get('h2').should('contain', 'Failed to import phenotips analysis');
    cy.get('.modal-container > span').should('contain', 'Error: Status Code: 409 Conflict');
    cy.get('.modal-container').should('exist');
    cy.get('[data-test="confirm-button"]').click();
    cy.get('.modal-container').should('not.exist');
  });

  it('tries to import a new case with a file that isn\'t a JSON file', () => {
    cy.get('.analysis-create-card').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/example_file_to_upload.txt', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();
    cy.get('h2').should('contain', 'Failed to import phenotips analysis');
    cy.get('.modal-container > span').should('contain', 'Error: Status Code: 500 Internal Server Error');
    cy.get('.modal-container').should('exist');
    cy.get('[data-test="confirm-button"]').click();
    cy.get('.modal-container').should('not.exist');
  });
});
