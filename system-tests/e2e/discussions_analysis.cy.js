describe('discussions_analysis.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.visit('/analysis/CPAM0002/#Discussion');
  });

  it('should have a discussion section', () => {
    cy.get('#Discussion').should('exist');
  });

  it('should publish a new post to the discussion section', () => {
    cy.get('[data-test="new-discussion-button"]').click();

    cy.get('[data-test="discussion-post"]').should('have.length', 3);

    cy.get('[data-test="new-discussion-input"]').type('System Test Text');
    cy.get('[data-test="new-discussion-publish"]').click();

    cy.get('[data-test="discussion-post"]').should('have.length', 4);
  });

  it('should not be able to publish a post with no text in the new discussion field', () => {
    cy.get('[data-test="new-discussion-button"]').click();
    cy.get('[data-test="new-discussion-publish"]').should('be.disabled');
  });

  it('should cancel a new post, close the new post field, and not post anything', () => {
    cy.get('[data-test="new-discussion-button"]').click();

    cy.get('[data-test="new-discussion-input"]').type('System Test Text');
    cy.get('[data-test="new-discussion-cancel"]').click();

    cy.get('[data-test="new-discussion-input"]').should('not.exist');

    cy.get('[data-test="discussion-post"]').should('have.length', 3);
  });

  it('should publish a new post to the discussion section then proceed to delete it successfully', () => {
    cy.get('[data-test="new-discussion-button"]').click();

    cy.get('[data-test="new-discussion-input"]').type('System Test Text');
    cy.get('[data-test="new-discussion-publish"]').click();

    cy.get('[data-test="discussion-post"]').should('have.length', 4);

    cy.get('[data-test="discussion-post"]').eq(3).as('newDiscussion');

    cy.get('@newDiscussion')
        .find('[data-test="discussion-post-context-menu"]')
        .click();

    cy.get('@newDiscussion')
        .find('.grey-rounded-menu > :nth-child(2)')
        .contains('Delete')
        .trigger('mouseover');

    cy.get('@newDiscussion')
        .find('.grey-rounded-menu > :nth-child(2)')
        .click();

    cy.get('[data-test="notification-dialog"]').find('[data-test="confirm-button"]').contains('Delete').click();

    cy.get('[data-test="discussion-post"]').should('have.length', 3);
  });

  it('should publish a new post to the discussion section, delete the post, and cancel the deletion', () => {
    cy.get('#Discussion').should('exist');

    cy.get('[data-test="new-discussion-button"]').click();

    cy.get('[data-test="new-discussion-input"]').type('System Test Text');
    cy.get('[data-test="new-discussion-publish"]').click();

    cy.get('[data-test="discussion-post"]').should('have.length', 4);

    cy.get('[data-test="discussion-post"]').eq(3).as('newDiscussion');

    cy.get('@newDiscussion')
        .find('[data-test="discussion-post-context-menu"]')
        .click();

    cy.get('@newDiscussion')
        .find('.grey-rounded-menu > :nth-child(2)')
        .contains('Delete')
        .click();

    cy.get('[data-test="notification-dialog"]').find('[data-test="cancel-button"]').contains('Cancel').click();

    cy.get('[data-test="discussion-post"]').should('have.length', 4);
  });

  it('Should proceed to edit an existing discussion post and save it', () => {
    cy.get('[data-test="new-discussion-button"').click();

    cy.get('[data-test="new-discussion-input"]').type('System Test Text');
    cy.get('[data-test="new-discussion-publish"]').click();

    cy.get('[data-test="discussion-post"]').should('have.length', 4);

    cy.get('[data-test="discussion-post"]').eq(3).as('existingDiscussion');

    cy.get('@existingDiscussion')
        .find('[data-test="discussion-post-context-menu"]')
        .click();

    cy.get('@existingDiscussion')
        .find('.grey-rounded-menu > :nth-child(1)')
        .contains('Edit')
        .click();

    cy.get('[data-test="edit-discussion-input"]').clear();
    cy.get('[data-test="edit-discussion-input"]').type('Editing a system test.');

    cy.get('[data-test="edit-discussion-save"]').click();

    cy.get('[data-test="discussion-post"]')
        .eq(3)
        .find('[data-test="discussion-post-content"]')
        .should('have.text', 'Editing a system test.');
  });

  it('Should proceed to edit a discussion post and then cancel it leaving the original post intact', () => {
    cy.get('[data-test="new-discussion-button"').click();

    cy.get('[data-test="new-discussion-input"]').type('System Test Text.');
    cy.get('[data-test="new-discussion-publish"]').click();

    cy.get('[data-test="discussion-post"]').should('have.length', 4);

    cy.get('[data-test="discussion-post"]').eq(3).as('existingDiscussion');

    cy.get('@existingDiscussion')
        .find('[data-test="discussion-post-context-menu"]')
        .click();

    cy.get('@existingDiscussion')
        .find('.grey-rounded-menu > :nth-child(1)')
        .contains('Edit')
        .trigger('mouseover');

    cy.get('@existingDiscussion')
        .find('.grey-rounded-menu > :nth-child(1)')
        .click();

    cy.get('[data-test="edit-discussion-input"]').clear();
    cy.get('[data-test="edit-discussion-input"]').type('Editing a system test.');

    cy.get('[data-test="edit-discussion-cancel"]').click();

    cy.get('[data-test="discussion-post"]')
        .eq(3)
        .find('[data-test="discussion-post-content"]')
        .should('have.text', 'System Test Text.');
  });
});
