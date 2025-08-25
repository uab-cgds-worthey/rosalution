describe('discussions_analysis.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.fixture('section-image-1.jpg', {encoding: null}).as('sectionImageJpg');
    cy.fixture('section-evidence-1.pdf', {encoding: null}).as('sectionEvidencePdf');
    cy.visit('/analysis/CPAM0002#Discussion');
  });

  it('should publish, edit, and delete posts to the discussion section', () => {
    cy.get('#Discussion').should('exist');

    cy.get('[data-test="new-discussion-button"]').click();

    // Verifies unable to submit empty post content
    cy.get('[data-test="new-discussion-publish"]').should('be.disabled');
    cy.get('[data-test="discussion-post"]').should('have.length', 3);

    // Supports canceling a new post
    cy.get('[data-test="new-discussion-input"]').type('System Test Text', {force: true});
    cy.get('[data-test="new-discussion-cancel"]').click();
    cy.get('[data-test="new-discussion-input"]').should('not.exist');
    cy.get('[data-test="discussion-post"]').should('have.length', 3);

    // Publish a new post
    cy.get('[data-test="new-discussion-button"]').click();
    cy.get('[data-test="new-discussion-input"]').type('System Test Text', {force: true});
    cy.get('[data-test="new-discussion-publish"]').click();
    cy.get('[data-test="discussion-post"]').should('have.length', 4);

    // Prompt to Delete but cancel
    cy.get('[data-test="discussion-post"]')
        .find('.grey-rounded-menu > :nth-child(2)')
        .contains('Delete')
        .click({force: true});

    cy.get('[data-test="notification-dialog"]').find('[data-test="cancel-button"]').contains('Cancel').click();
    cy.get('[data-test="discussion-post"]').should('have.length', 4);

    // Delete and confirm deleting post
    cy.get('[data-test="discussion-post"]')
        .eq(3)
        .find('[data-test="discussion-post-header"]')
        .find('[data-test="discussion-post-context-menu"]')
        .click({force: true});
    cy.get('[data-test="discussion-post"]')
        .find('.grey-rounded-menu > :nth-child(2)')
        .contains('Delete')
        .click({force: true});
    cy.get('[data-test="notification-dialog"]').find('[data-test="confirm-button"]').contains('Delete').click();
    cy.get('[data-test="discussion-post"]').should('have.length', 3);
  });

  it('should allow attaching new files, links, and existing attachments to new posts', () => {
    cy.get('#Discussion').should('exist');

    // Attach a single file to a new post
    cy.get('[data-test="new-discussion-button"]').click();
    cy.get('[data-test="new-discussion-input"]').type('System Test Text with single file', {force: true});
    cy.get('[data-test="discussion-attachment-button"]').click();
    cy.get('.modal-container')
        .find('[data-test="button-input-dialog-upload-file"]')
        .click();
    cy.get('.drop-file-box-content').selectFile('@sectionEvidencePdf', {action: 'drag-drop'});
    cy.get('.modal-container').find('[data-test="confirm"]').click();
    cy.get('[data-test="new-discussion-publish"]').click();
    cy.get('[data-test="discussion-post"]').should('have.length', 4);

    // Attach multiple new files
    cy.get('[data-test="new-discussion-button"]').click();
    cy.get('[data-test="new-discussion-input"]').type('System Test Text with single file');
    cy.get('[data-test="discussion-attachment-button"]').click();
    cy.get('.modal-container')
        .find('[data-test="button-input-dialog-upload-file"]')
        .click();
    cy.get('.drop-file-box-content').selectFile('@sectionEvidencePdf', {action: 'drag-drop'});
    cy.get('.modal-container').find('[data-test="confirm"]').click();
    cy.get('[data-test="discussion-attachment-button"]').click();
    cy.get('.modal-container')
        .find('[data-test="button-input-dialog-upload-file"]')
        .click();
    cy.get('.drop-file-box-content').selectFile('@sectionImageJpg', {action: 'drag-drop'});
    cy.get('.modal-container').find('[data-test="confirm"]').click();
    cy.get('[data-test="new-discussion-publish"]').click();
    cy.get('[data-test="discussion-post"]').should('have.length', 5);

    // Attach new link attachment
    cy.get('[data-test="new-discussion-button"]').click();
    cy.get('[data-test="new-discussion-input"]').type('System Test Text with single link', {force: true});
    cy.get('[data-test="discussion-attachment-button"]').click();
    cy.get('.modal-container')
        .find('[data-test="button-input-dialog-attach-url"]')
        .click();
    cy.get('[data-test="name-input"]').type('Best research team ever');
    cy.get('[data-test="link-input"]').type('https://sites.uab.edu/cgds');
    cy.get('.modal-container').find('[data-test="confirm"]').click();
    cy.get('[data-test="new-discussion-publish"]').click();
    cy.get('[data-test="discussion-post"]').should('have.length', 6);

    // Attach new link attachment
    cy.get('[data-test="new-discussion-button"]').click();
    cy.get('[data-test="new-discussion-input"]').type('System Test Text with single link', {force: true});
    cy.get('[data-test="discussion-attachment-button"]').click();
    cy.get('.modal-container')
        .find('[data-test="button-input-dialog-attach-url"]')
        .click();
    cy.get('[data-test="name-input"]').type('Best research team ever');
    cy.get('[data-test="link-input"]').type('https://sites.uab.edu/cgds');
    cy.get('.modal-container').find('[data-test="confirm"]').click();
    cy.get('[data-test="new-discussion-publish"]').click();

    cy.get('[data-test="discussion-post"]').should('have.length', 7);
  });

  it('Should proceed to edit an existing discussion post and save it', () => {
    cy.get('[data-test="new-discussion-button"').click();

    cy.get('[data-test="new-discussion-input"]').type('System Test Text.', {force: true});
    cy.get('[data-test="new-discussion-publish"]').click();
    cy.get('[data-test="discussion-post"]').should('have.length', 4);

    // Edit then cancel editing
    cy.get('[data-test="discussion-post"]')
        .eq(2)
        .find('[data-test="discussion-post-header"]')
        .find('[data-test="discussion-post-context-menu"]')
        .click({force: true});

    cy.get('[data-test="discussion-post"]')
        .find('.grey-rounded-menu > :nth-child(1)')
        .contains('Edit')
        .click({force: true});

    cy.get('[data-test="edit-discussion-input"]').clear();
    cy.get('[data-test="edit-discussion-input"]').type('Editing a system test.');

    cy.get('[data-test="edit-discussion-cancel"]').click();

    // Publish editted post
    cy.get('#Discussion').scrollIntoView();
    cy.get('[data-test="new-discussion-button"').click();
    cy.get('[data-test="discussion-post"]')
        .eq(3)
        .find('[data-test="discussion-post-content"]')
        .should('have.text', 'System Test Text.');

    cy.get('[data-test="discussion-post"]')
        .eq(3)
        .find('[data-test="discussion-post-header"]')
        .find('[data-test="discussion-post-context-menu"]')
        .click({force: true});

    cy.get('[data-test="discussion-post"]')
        .find('.grey-rounded-menu > :nth-child(1)')
        .contains('Edit')
        .click({force: true});

    cy.get('[data-test="edit-discussion-input"]').clear();
    cy.get('[data-test="edit-discussion-input"]').type('Editing a system test.');

    cy.get('[data-test="edit-discussion-save"]').click({force: true});

    cy.get('[data-test="discussion-post"]')
        .eq(2)
        .find('[data-test="discussion-post-content"]')
        .should('have.text', 'Editing a system test.');
  });
});
