const path = require("path");

describe('case_supporting_evidence.cy.js', () => {
  const downloadsFolder = Cypress.config("downloadsFolder");

  beforeEach(() => {
    cy.resetDatabase();
    cy.visit('/');
    cy.get('.analysis-card').first().click();
    cy.get('[href="#Supporting_Evidence"]').click();
  });

  it('attaches a supporting evidence link to an analysis case and can download', () => {
    cy.get('#Supporting_Evidence').should('exist');
    cy.get('.attachment-list').should('have.length', 0);
    cy.get('[data-test="add-button"]').click();
    cy.get('[data-test="button-input-dialog-attach-url"]').click();
    cy.get('[data-test="name-input"]').type('test link to google');
    cy.get('[data-test="link-input"]').type('https://www.google.com');
    cy.get('[data-test="comments-text-area"]').type('this is a test comment for a test link to google');
    cy.get('[data-test="confirm"]').click();
    cy.get('[href="#Supporting_Evidence"]').click();
    cy.get('.attachment-list').should('have.length', 1);
    cy.get('.attachment-name').should('have.text', 'test link to google');
    cy.get('.attachment-name > a').should('have.attr', 'href', 'https://www.google.com');
    cy.get('.attachment-name > a').should('have.attr', 'target', '_blank');
    cy.get('.attachment-name > a').should('have.attr', 'rel', 'noreferrer noopener');
    cy.get('.attachment-name > a').then((link) => {
      cy.request(link.prop('href')).its('status').should('eq', 200);
    });
  });

  it('attaches a supporting evidence link to an analysis case and edits it', () => {
    cy.get('#Supporting_Evidence').should('exist');
    cy.get('.attachment-list').should('have.length', 0);
    cy.get('[data-test="add-button"]').click();
    cy.get('[data-test="button-input-dialog-attach-url"]').click();
    cy.get('[data-test="name-input"]').type('test link to google');
    cy.get('[data-test="link-input"]').type('https://www.google.com');
    cy.get('[data-test="comments-text-area"]').type('this is a test comment for a test link to google');
    cy.get('[data-test="confirm"]').click();
    cy.get('[href="#Supporting_Evidence"]').click();
    cy.get('.attachment-list').should('have.length', 1);
    cy.get('.attachment-name').should('have.text', 'test link to google');
    cy.get('.attachment-name > a').should('have.attr', 'href', 'https://www.google.com');
    cy.get('.attachment-name > a').should('have.attr', 'target', '_blank');
    cy.get('.attachment-name > a').should('have.attr', 'rel', 'noreferrer noopener');
    cy.get('.attachment-name > a').then((link) => {
      cy.request(link.prop('href')).its('status').should('eq', 200);
    });
    cy.get('[href="#Supporting_Evidence"]').click();
    cy.get('.edit-button').click();
    cy.get('[data-test="name-input"]').clear().type('test link to uab.edu');
    cy.get('[data-test="link-input"]').clear().type('https://www.uab.edu/home/');
    cy.get('[data-test="comments-text-area"]').clear().type('this is a test comment for a test link to uab.edu');
    cy.get('[data-test="confirm"]').click();
    cy.get('[href="#Supporting_Evidence"]').click();
    cy.get('.attachment-list').should('have.length', 1);
    cy.get('.attachment-name > a').should('have.attr', 'href', 'https://www.uab.edu/home/');
    cy.get('.attachment-name > a').should('have.attr', 'target', '_blank');
    cy.get('.attachment-name > a').should('have.attr', 'rel', 'noreferrer noopener');
    cy.get('.attachment-name > a').then((link) => {
      cy.request(link.prop('href')).its('status').should('eq', 200);
    });
    cy.get('.attachment-comments').should('have.text', 'this is a test comment for a test link to uab.edu');
  });

  it('attaches a supporting evidence link to an analysis case and can delete it', () => {
    cy.get('#Supporting_Evidence').should('exist');
    cy.get('.attachment-list').should('have.length', 0);
    cy.get('[data-test="add-button"]').click();
    cy.get('[data-test="button-input-dialog-attach-url"]').click();
    cy.get('[data-test="name-input"]').type('test link to google');
    cy.get('[data-test="link-input"]').type('https://www.google.com');
    cy.get('[data-test="comments-text-area"]').type('this is a test comment for a test link to google');
    cy.get('[data-test="confirm"]').click();
    cy.get('[href="#Supporting_Evidence"]').click();
    cy.get('.attachment-list').should('have.length', 1);
    cy.get('.attachment-name').should('have.text', 'test link to google');
    cy.get('.attachment-name > a').should('have.attr', 'href', 'https://www.google.com');
    cy.get('.attachment-name > a').should('have.attr', 'target', '_blank');
    cy.get('.attachment-name > a').should('have.attr', 'rel', 'noreferrer noopener');
    cy.get('.attachment-name > a').then((link) => {
      cy.request(link.prop('href')).its('status').should('eq', 200);
    });
    cy.get('.delete-button').click();
    cy.get('.modal-container').should('exist');
    cy.get('[data-test="confirm-button"]').click();
    cy.get('.attachment-list').should('have.length', 0);
  });

  it('attaches a supporting evidence file to an analysis case, downloads, and asserts the file exists', () => {
    cy.get('#Supporting_Evidence').should('exist');
    cy.get('.attachment-list').should('have.length', 0);
    cy.get('[data-test="add-button"]').click();
    cy.get('[data-test="button-input-dialog-upload-file"]').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/pedigree-fake.jpg', {
      action: 'drag-drop',
    });
    cy.get('.comments').type('this is a test comment for a test file');
    cy.get('[data-test="confirm"]').click();
    cy.get('[href="#Supporting_Evidence"]').click();
    cy.get('.attachment-list').should('have.length', 1);
    cy.get('.attachment-name > div').should('have.attr', 'target', '_blank');
    cy.get('.attachment-name > div').should('have.attr', 'rel', 'noreferrer noopener');
    cy.get('.attachment-name > div').click()
    cy.readFile(path.join(downloadsFolder, 'pedigree-fake.jpg'))
  });

  it('attaches a supporting evidence file to an analysis case and can edit the comments', () => {
    cy.get('#Supporting_Evidence').should('exist');
    cy.get('.attachment-list').should('have.length', 0);
    cy.get('[data-test="add-button"]').click();
    cy.get('[data-test="button-input-dialog-upload-file"]').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/pedigree-fake.jpg', {
      action: 'drag-drop',
    });
    cy.get('.comments').type('this is a test comment for a test file');
    cy.get('[data-test="confirm"]').click();
    cy.get('[href="#Supporting_Evidence"]').click();
    cy.get('.attachment-list').should('have.length', 1);
    cy.get('.attachment-name > div').should('have.attr', 'target', '_blank');
    cy.get('.attachment-name > div').should('have.attr', 'rel', 'noreferrer noopener');
    cy.get('.edit-button').click();
    cy.get('.comments').clear().type('this is a test comment for a test file edited');
    cy.get('[data-test="confirm"]').click();
    cy.get('[href="#Supporting_Evidence"]').click();
    cy.get('.attachment-list').should('have.length', 1);
    cy.get('.attachment-name > div').should('have.attr', 'target', '_blank');
    cy.get('.attachment-name > div').should('have.attr', 'rel', 'noreferrer noopener');
    cy.get('.attachment-comments').should('have.text', 'this is a test comment for a test file edited');
  });

  it('attaches a supporting evidence file to an analysis case and can delete it', () => {
    cy.get('#Supporting_Evidence').should('exist');
    cy.get('.attachment-list').should('have.length', 0);
    cy.get('[data-test="add-button"]').click();
    cy.get('[data-test="button-input-dialog-upload-file"]').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/pedigree-fake.jpg', {
      action: 'drag-drop',
    });
    cy.get('.comments').type('this is a test comment for a test file');
    cy.get('[data-test="confirm"]').click();
    cy.get('[href="#Supporting_Evidence"]').click();
    cy.get('.attachment-list').should('have.length', 1);
    cy.get('.attachment-name > div').should('have.attr', 'target', '_blank');
    cy.get('.attachment-name > div').should('have.attr', 'rel', 'noreferrer noopener');
    cy.get('.delete-button').click();
    cy.get('.modal-container').should('exist');
    cy.get('[data-test="confirm-button"]').click();
    cy.get('.attachment-list').should('have.length', 0);
  });

  it('should fail to attach the same supporting evidence file twice to the same analysis', () => {
    cy.get('#Supporting_Evidence').should('exist');
    cy.get('.attachment-list').should('have.length', 0);
    cy.get('[data-test="add-button"]').click();
    cy.get('[data-test="button-input-dialog-upload-file"]').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/pedigree-fake.jpg', {
      action: 'drag-drop',
    });
    cy.get('.comments').type('this is a test comment for a test file');
    cy.get('[data-test="confirm"]').click();
    cy.get('[href="#Supporting_Evidence"]').click();
    cy.get('.attachment-list').should('have.length', 1);
    cy.get('.attachment-name > div').should('have.attr', 'target', '_blank');
    cy.get('.attachment-name > div').should('have.attr', 'rel', 'noreferrer noopener');
    cy.get('[data-test="add-button"]').click();
    cy.get('[data-test="button-input-dialog-upload-file"]').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/pedigree-fake.jpg', {
      action: 'drag-drop',
    });
    cy.get('.comments').type('this is a test comment for a test file');
    cy.get('[data-test="confirm"]').click();
    cy.get('.attachment-list').should('have.length', 1);
  });

  it('should be able to attach the same supporting evidence file to different analyses', () => {
    cy.get('#Supporting_Evidence').should('exist');
    cy.get('.attachment-list').should('have.length', 0);
    cy.get('[data-test="add-button"]').click();
    cy.get('[data-test="button-input-dialog-upload-file"]').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/pedigree-fake.jpg', {
      action: 'drag-drop',
    });
    cy.get('.comments').type('this is a test comment for a test file');
    cy.get('[data-test="confirm"]').click();
    cy.get('[href="#Supporting_Evidence"]').click();
    cy.get('.attachment-list').should('have.length', 1);
    cy.get('.attachment-name > div').should('have.attr', 'target', '_blank');
    cy.get('.attachment-name > div').should('have.attr', 'rel', 'noreferrer noopener');

    cy.get('.rosalution-logo').click();
    cy.get('[href="/rosalution/analysis/CPAM0046"] > .analysis-card > .analysis-base').click();
    cy.get('[href="#Supporting_Evidence"]').click();
    cy.get('.attachment-list').should('have.length', 0);
    cy.get('[data-test="add-button"]').click();
    cy.get('[data-test="button-input-dialog-upload-file"]').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/pedigree-fake.jpg', {
      action: 'drag-drop',
    });
    cy.get('.comments').type('this is a test comment for a test file');
    cy.get('[data-test="confirm"]').click();
    cy.get('[href="#Supporting_Evidence"]').click();
    cy.get('.attachment-list').should('have.length', 1);
    cy.get('.attachment-name > div').should('have.attr', 'target', '_blank');
    cy.get('.attachment-name > div').should('have.attr', 'rel', 'noreferrer noopener');
  });
});
