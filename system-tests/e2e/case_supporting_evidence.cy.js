import * as path from 'path';

describe('analysis_attahments.cy.js', () => {
  const downloadsFolder = Cypress.config('downloadsFolder');

  beforeEach(() => {
    cy.resetDatabase();
    cy.intercept('/rosalution/api/analysis/CPAM0002/attachment').as('attachmentOperation');
    cy.visit('analysis/CPAM0002#Attachments');
  });

  it('attaches a links and files to analyses that can be edited and/or removd ', () => {
    cy.get('#Attachments').should('exist');
    cy.get('.attachment-list').should('have.length', 0);
    cy.get('[data-test="add-button"]').click();
    cy.get('[data-test="button-input-dialog-attach-url"]').click();
    cy.get('[data-test="name-input"]').type('test link to google');
    cy.get('[data-test="link-input"]').type('https://www.google.com');
    cy.get('[data-test="comments-text-area"]').type('this is a test comment for a test link to google');
    cy.get('[data-test="confirm"]').click();
    cy.wait('@attachmentOperation');
    cy.get('[href="#Attachments"]').click();
    cy.get('.attachment-list').should('have.length', 3);
    cy.get('.attachment-name').eq(2).should('have.text', 'test link to google');
    cy.get('.attachment-name > a')
        .eq(2)
        .should('have.attr', 'href', 'https://www.google.com')
        .should('have.attr', 'target', '_blank')
        .should('have.attr', 'rel', 'noreferrer noopener')
        .then((link) => {
          cy.request(link.prop('href')).its('status').should('eq', 200);
        });

    cy.get('[data-test="edit-button"]').eq(2).click();
    cy.get('[data-test="name-input"]').clear();
    cy.get('[data-test="name-input"]').type('test link to uab.edu');
    cy.get('[data-test="link-input"]').clear();
    cy.get('[data-test="link-input"]').type('https://www.uab.edu/home/');
    cy.get('[data-test="comments-text-area"]').clear();
    cy.get('[data-test="comments-text-area"]').type('this is a test comment for a test link to uab.edu');
    cy.get('[data-test="confirm"]').click();
    cy.get('[href="#Attachments"]').click();
    cy.get('.attachment-list').should('have.length', 3);
    cy.get('.attachment-name > a')
        .eq(2)
        .should('have.attr', 'href', 'https://www.uab.edu/home/')
        .should('have.attr', 'target', '_blank')
        .should('have.attr', 'rel', 'noreferrer noopener')
        .then((link) => {
          cy.request(link.prop('href')).its('status').should('eq', 200);
        });
    cy.get('.attachment-comments').eq(2).should('have.text', 'this is a test comment for a test link to uab.edu');
    cy.get('[data-test="delete-button"]').eq(2).click();
    cy.get('.modal-container').should('exist');
    cy.get('[data-test="confirm-button"]').click();
    cy.get('.attachment-list').should('have.length', 2);
    cy.get('[data-test="add-button"]').click();
    cy.get('[data-test="button-input-dialog-upload-file"]').click();
    cy.get('.drop-file-box-content').selectFile('fixtures/example-family-pedigree.png', {
      action: 'drag-drop',
    });
    cy.get('.comments').type('this is a test comment for a test file');
    cy.get('[data-test="confirm"]').click();
    cy.get('[href="#Attachments"]').click();
    cy.get('.attachment-list').should('have.length', 3);
    cy.get('.attachment-name > div')
        .should('have.attr', 'target', '_blank')
        .should('have.attr', 'rel', 'noreferrer noopener');
    cy.get('.attachment-name > div').click();
    cy.readFile(path.join(downloadsFolder, 'example-family-pedigree.png'));

    cy.get('[data-test="edit-button"]').eq(2).click();
    cy.get('.comments').clear();
    cy.get('.comments').type('this is a test comment for a test file edited');
    cy.get('[data-test="confirm"]').click();

    cy.get('[href="#Attachments"]').click();
    cy.get('.attachment-list').should('have.length', 3);
    cy.get('.attachment-name > div')
        .should('have.attr', 'target', '_blank')
        .should('have.attr', 'rel', 'noreferrer noopener');
    cy.get('.attachment-comments')
        .eq(2)
        .should('have.text', 'this is a test comment for a test file edited');

    cy.get('[data-test="delete-button"]').eq(2).click();
    cy.get('.modal-container').should('exist');
    cy.get('[data-test="confirm-button"]').click();
    cy.get('.attachment-list').should('have.length', 2);

    // Attaching Same File again
    cy.get('[data-test="add-button"]').click();
    cy.get('[data-test="button-input-dialog-upload-file"]').click();
    cy.get('.drop-file-box-content').selectFile('fixtures/example-family-pedigree.png', {
      action: 'drag-drop',
    });
    cy.get('.comments').type('this is a test comment for a test file');
    cy.get('[data-test="confirm"]').click();
    cy.get('.attachment-list').should('have.length', 3);

    // Visit another Analysis and attachment same file.
    cy.visit('analysis/CPAM0046#Attachments');
    cy.get('.attachment-list').should('have.length', 0);
    cy.get('[data-test="add-button"]').click();
    cy.get('[data-test="button-input-dialog-upload-file"]').click();
    cy.get('.drop-file-box-content').selectFile('fixtures/example-family-pedigree.png', {
      action: 'drag-drop',
    });
    cy.get('.comments').type('writing a different comment and testing this out.');
    cy.get('[data-test="confirm"]').click();
    cy.get('[href="#Attachments"]').click();
    cy.get('.attachment-list').should('have.length', 1);
    cy.get('.attachment-name > div')
        .should('have.attr', 'target', '_blank')
        .should('have.attr', 'rel', 'noreferrer noopener')
        .should('have.text', 'example-family-pedigree.png');
    cy.get('.attachment-comments').should('have.text', 'writing a different comment and testing this out.');
  });
});
