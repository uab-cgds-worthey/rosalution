import * as path from 'path';

describe('Case Model System', () => {
  const downloadsFolder = Cypress.config('downloadsFolder');

  beforeEach(() => {
    cy.resetDatabase();
    cy.login('vrr-prep');
    cy.intercept('/rosalution/api/analysis/CPAM0002').as('analysisLoad');
    cy.visit('analysis/CPAM0002');
  });

  it('Should attach file to the Mouse Model Systems Veterinary Histology Report', () => {
    cy.get('[data-test="user-menu"]')
        .find('.grey-rounded-menu')
        .as('userActionMenu')
        .invoke('attr', 'style', 'display: block; visibility: visible; opacity: 1;');
    cy.get('@userActionMenu').contains('Edit').click();
    cy.get('@userActionMenu').invoke('attr', 'style', 'display: block; visibility: hidden; opacity: 0;');
    cy.wait('@analysisLoad');
    cy.get('[href="#Mus_musculus (Mouse) Model System"]').click();

    cy.get('[data-test="Veterinary Histology Report"]')
        .find('[data-test="attach-button-Veterinary Histology Report"]')
        .click();
    cy.get('.modal-container')
        .find('[data-test="button-input-dialog-upload-file"]')
        .click();

    cy.get('.drop-file-box-content').selectFile('fixtures/section-evidence-1.pdf', {action: 'drag-drop'});
    cy.get('.modal-container').find('[data-test="confirm"]').click();

    cy.get('[data-test="Veterinary Histology Report"]')
        .find('[data-test="section-attachment-Veterinary Histology Report"]')
        .find('.attachment-name')
        .should('have.text', 'section-evidence-1.pdf')
        .click();

    cy.readFile(path.join(downloadsFolder, 'section-evidence-1.pdf'));
  });

  it('Should attach a Veterinary Histology Report, delete it, add different file, downloads', () => {
    // Make the user menu visible, click the edit button in the menu to make the analysis editable, then close the menu
    cy.get('[data-test="user-menu"]')
        .find('.grey-rounded-menu')
        .invoke('attr', 'style', 'display: block; visibility: visible; opacity: 1;');
    cy.get('[data-test="user-menu"] > .grey-rounded-menu').contains('Edit').click();
    cy.get('[data-test="user-menu"]')
        .find('.grey-rounded-menu')
        .invoke('attr', 'style', 'display: block; visibility: hidden; opacity: 0;');

    // Find the Mouse Model System section and upload a Histology Report
    cy.get('[href="#Mus_musculus (Mouse) Model System"]').click();
    cy.get('[data-test="Veterinary Histology Report"]')
        .find('[data-test="attach-button-Veterinary Histology Report"]')
        .click();
    cy.get('.modal-container')
        .find('[data-test="button-input-dialog-upload-file"]')
        .click();
    cy.get('.drop-file-box-content').selectFile('fixtures/section-evidence-1.pdf', {
      action: 'drag-drop',
    });
    cy.get('.modal-container').find('[data-test="confirm"]').click();
    cy.get('.save-modal-container').find('[data-test="save-edit-button"]').click();
    cy.wait('@analysisLoad');

    // Realize it's the wrong report and delete it from the section attachment field
    cy.get('[data-test="Veterinary Histology Report"]').find('[data-test="delete-button"]').click();
    cy.get('.modal-container').find('[data-test="confirm-button"]').click();

    // Make the user menu visible, click the edit button in the menu to make the analysis editable, then close the menu
    cy.get('[data-test="user-menu"]')
        .find('.grey-rounded-menu')
        .invoke('attr', 'style', 'display: block; visibility: visible; opacity: 1;');
    cy.get('[data-test="user-menu"] > .grey-rounded-menu').contains('Edit').click();
    cy.get('[data-test="user-menu"]')
        .find('.grey-rounded-menu')
        .invoke('attr', 'style', 'display: block; visibility: hidden; opacity: 0;');

    // Upload a new section attachment that's the correct report
    cy.get('[data-test="Veterinary Histology Report"]')
        .find('[data-test="attach-button-Veterinary Histology Report"]')
        .click();
    cy.get('.modal-container')
        .find('[data-test="button-input-dialog-upload-file"]')
        .click();
    cy.get('.drop-file-box-content').selectFile('fixtures/section-evidence-2.pdf', {
      action: 'drag-drop',
    });
    cy.get('.modal-container').find('[data-test="confirm"]').click();
    cy.get('.save-modal-container').find('[data-test="save-edit-button"]').click();
    cy.wait('@analysisLoad');

    // Ensure that the second report is the report that was uploaded
    cy.get('[data-test="Veterinary Histology Report"]')
        .find('[data-test="section-attachment-Veterinary Histology Report"]')
        .find('.attachment-name')
        .should('have.text', 'section-evidence-2.pdf')
        .click();

    cy.readFile(path.join(downloadsFolder, 'section-evidence-2.pdf'));
  });

  it('Should attach URL for Mouse Model Systems Veterinary Pathology Imaging and click to verify', () => {
    cy.get('[data-test="user-menu"]')
        .find('.grey-rounded-menu')
        .invoke('attr', 'style', 'display: block; visibility: visible; opacity: 1;');
    cy.get('[data-test="user-menu"] > .grey-rounded-menu').contains('Edit').click();
    cy.get('[data-test="user-menu"]')
        .find('.grey-rounded-menu')
        .invoke('attr', 'style', 'display: block; visibility: hidden; opacity: 0;');
    cy.get('[href="#Mus_musculus (Mouse) Model System"]').click();

    cy.get('[data-test="section-attachment-Veterinary Pathology Imaging"]')
        .find('[data-test="attach-button-Veterinary Pathology Imaging"]')
        .click();
    cy.get('.modal-container').find('[data-test="name-input"]').type('VMA21 Histology Slides');
    cy.get('.modal-container').find('[data-test="link-input"]').type('https://www.google.com');

    cy.get('.modal-container').find('[data-test="confirm"]').click();

    cy.get('[data-test="section-attachment-Veterinary Pathology Imaging"]')
        .find('.attachment-name')
        .should('have.text', 'VMA21 Histology Slides');

    cy.get('[data-test="section-attachment-Veterinary Pathology Imaging"]').find('.attachment-name').then((link) => {
      cy.request(link.prop('href')).its('status').should('eq', 200);
    });
  });

  it('Should attach URL to the Veterinary Pathology Imaging,then deletes URL, adds another, verifies', () => {
    // Make the menu visible, click edit button to make the menu analysis editable, then close the menu
    cy.get('[data-test="user-menu"]')
        .find('.grey-rounded-menu')
        .invoke('attr', 'style', 'display: block; visibility: visible; opacity: 1;');
    cy.get('[data-test="user-menu"] > .grey-rounded-menu').contains('Edit').click();
    cy.get('[data-test="user-menu"]')
        .find('.grey-rounded-menu')
        .invoke('attr', 'style', 'display: block; visibility: hidden; opacity: 0;');
    cy.wait('@analysisLoad');

    // Find the Mouse Model System section and add a Pathology Imaging Slide link
    cy.get('[href="#Mus_musculus (Mouse) Model System"]').click();
    cy.get('[data-test="section-attachment-Veterinary Pathology Imaging"]')
        .find('[data-test="attach-button-Veterinary Pathology Imaging"]')
        .click();
    cy.get('.modal-container').find('[data-test="name-input"]').type('VMA21 Pathology Slides');
    cy.get('.modal-container').find('[data-test="link-input"]').type('https://www.google.com');
    cy.get('.modal-container').find('[data-test="confirm"]').click();

    // Save the edit and close editing mode
    cy.get('.save-modal-container').find('[data-test="save-edit-button"]').click();
    cy.wait('@analysisLoad');
    cy.get('[href="#Mus_musculus (Mouse) Model System"]').click();

    // Find the Pathology Imaging section again and delete the existing link
    cy.get('[data-test="Veterinary Pathology Imaging"]')
        .find('[data-test="delete-button"]')
        .click();
    cy.get('.modal-container')
        .find('[data-test="confirm-button"]')
        .click();

    // Make the menu visible, click edit button to make the menu analysis editable, then close the menu
    cy.get('[data-test="user-menu"]')
        .find('.grey-rounded-menu')
        .invoke('attr', 'style', 'display: block; visibility: visible; opacity: 1;');
    cy.get('[data-test="user-menu"] > .grey-rounded-menu').contains('Edit').click();
    cy.get('[data-test="user-menu"]')
        .find('.grey-rounded-menu')
        .invoke('attr', 'style', 'display: block; visibility: hidden; opacity: 0;');
    // cy.wait('@analysisLoad');

    //
    cy.get('[data-test="Veterinary Pathology Imaging"]')
        .find('[data-test="attach-button-Veterinary Pathology Imaging"]')
        .click();
    cy.get('.modal-container').find('[data-test="name-input"]').type('VMA21 Pathology Slides - Mouse Model');
    cy.get('.modal-container').find('[data-test="link-input"]').type('https://www.apple.com');
    cy.get('.modal-container').find('[data-test="confirm"]').click();

    // Save the edit and close editing mode
    cy.get('.save-modal-container').find('[data-test="save-edit-button"]').click();
    cy.wait('@analysisLoad');
    cy.get('[href="#Mus_musculus (Mouse) Model System"]').click();

    cy.get('[data-test="section-attachment-Veterinary Pathology Imaging"]')
        .find('.attachment-name')
        .should('have.text', 'VMA21 Pathology Slides - Mouse Model');

    cy.get('[data-test="section-attachment-Veterinary Pathology Imaging"]').find('.attachment-name').then((link) => {
      cy.request(link.prop('href')).its('status').should('eq', 200);
    });
  });
});
