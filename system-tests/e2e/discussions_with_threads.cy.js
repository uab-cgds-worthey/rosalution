describe('discussions_with_threads.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.fixture('section-image-1.jpg', {encoding: null}).as('sectionImage1');
    cy.fixture('section-evidence-1.pdf', {encoding: null}).as('sectionEvidence1');
    cy.intercept('/rosalution/api/analysis/CPAM0002').as('analysisLoad');
    cy.visit('/analysis/CPAM0002#Discussion');
    cy.wait('@analysisLoad');
  });

  it('should publish, edit, and delete replies in a post to the discussion section', () => {
    cy.get('#Discussion').should('exist');

    cy.get('[data-test="discussion-new-reply-button"')
        .eq(0)
        .click();

    // Verifies unable to submit empty reply content
    cy.get('[data-test="discussion-new-reply-publish"]').should('be.disabled');
    cy.get('[data-test="discussion-reply"]').should('have.length', 5);

    // Supports canceling a new reply
    cy.get('[data-test="discussion-new-reply-text-area"]').type('System Test Text', {force: true});
    cy.get('[data-test="new-discussion-reply-cancel-button"]').click();
    cy.get('[data-test="discussion-new-reply-text-area"]').should('not.exist');
    cy.get('[data-test="discussion-reply"]').should('have.length', 5);

    // Publish a new reply
    cy.get('[data-test="discussion-new-reply-button"]')
        .eq(0)
        .click();
    cy.get('[data-test="discussion-new-reply-text-area"]').type('System Test Text New Reply', {force: true});
    cy.get('[data-test="discussion-new-reply-publish"]').click();
    cy.get('[data-test="discussion-reply"]').should('have.length', 6);

    cy.get('[data-test="discussion-post-container"]')
        .eq(0)
        .find('[data-test="discussion-reply"]')
        .contains('System Test Text New Reply')
        .should('exist');

    // Prompt to Delete but cancel
    cy.get('[data-test="discussion-reply"]')
        .eq(2)
        .find('[data-test="discussion-reply-context-menu"]')
        .contains('Delete')
        .click({force: true});

    cy.get('[data-test="discussion-reply"]').should('have.length', 5);
    cy.get('[data-test="discussion-reply"]').contains('System Test Text New Reply').should('not.exist');
  });

  it('should allow attaching new files, links, and existing attachments to new posts', () => {
    cy.get('#Discussion').should('exist');

    // Attach multiple new files to a new reply
    cy.get('[data-test="discussion-new-reply-button"]')
        .eq(0)
        .click();
    cy.get('[data-test="discussion-new-reply-text-area"]').type('System Test with multiple new files', {force: true});
    cy.get('[data-test="discussion-reply-attachment-button"').click();
    cy.get('.modal-container')
        .find('[data-test="button-input-dialog-upload-file"]')
        .click();
    cy.get('.drop-file-box-content').selectFile('@sectionEvidence1', {action: 'drag-drop'});
    cy.get('.modal-container').find('[data-test="confirm"]').click();
    cy.get('[data-test="discussion-reply-attachment-button"]').click();
    cy.get('.modal-container')
        .find('[data-test="button-input-dialog-upload-file"]')
        .click();
    cy.get('.drop-file-box-content').selectFile('@sectionImage1', {action: 'drag-drop'});
    cy.get('.modal-container').find('[data-test="confirm"]').click();
    cy.get('[data-test="discussion-new-reply-publish"]').click();
    cy.get('[data-test="discussion-reply"]').should('have.length', 6);

    cy.get('[data-test="discussion-post-container"]')
        .eq(0)
        .find('[data-test="discussion-reply"]')
        .eq(2)
        .as('thirdReply');

    cy.get('@thirdReply').find('[data-test="discussion-attachment"]').should('have.length', 2);
    cy.get('@thirdReply').contains('System Test with multiple new files').should('exist');
  });

  it.only('Should soft delete post with thread and not delete thread', () => {
    cy.get('#Discussion').should('exist');
    cy.get('[data-test="discussion-post"]').should('have.length', 3);

    // Create new thread reply on last post
    cy.get('[data-test="discussion-new-reply-button"')
        .last()
        .click();

    cy.get('[data-test="discussion-new-reply-text-area"]').type('System Test Text New Reply', {force: true});
    cy.get('[data-test="discussion-new-reply-publish"]').click();
    cy.get('[data-test="discussion-reply"]').should('have.length', 6);

    // Delete the last post
    cy.get('[data-test="discussion-post"]')
        .last()
        .find('[data-test="discussion-post-header"]')
        .find('[data-test="discussion-post-context-menu"]')
        .click({force: true});
    cy.get('[data-test="discussion-post"]')
        .find('.grey-rounded-menu > :nth-child(2)')
        .contains('Delete')
        .click({force: true});
    cy.get('[data-test="notification-dialog"]').find('[data-test="confirm-button"]').contains('Delete').click();
    cy.get('[data-test="discussion-post"]')
        .should('have.length', 3)
        .last()
        .contains('[ This post was deleted. ]')
        .should('exist');
  });
});
