describe('discussions_analysis.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.visit('/analysis/CPAM0002#Discussion');
  });

  it('should publish a new post to the discussion section', () => {
    cy.get('#Discussion').should('exist');

    cy.get('[data-test="new-discussion-button"]').click();

    cy.get('[data-test="discussion-post"]').should('have.length', 3);

    cy.get('[data-test="new-discussion-input"]').type('System Test Text');
    cy.get('[data-test="new-discussion-publish"]').click();

    cy.get('[data-test="discussion-post"]').should('have.length', 4);
  });

  it('should not be able to publish a post with no text in the new discussion field', () => {
    cy.get('#Discussion').should('exist');

    cy.get('[data-test="new-discussion-button"]').click();
    cy.get('[data-test="new-discussion-publish"]').should('be.disabled');
  });

  it('should cancel a new post, close the new post field, and not post anything', () => {
    cy.get('#Discussion').should('exist');

    cy.get('[data-test="new-discussion-button"]').click();

    cy.get('[data-test="new-discussion-input"]').type('System Test Text');
    cy.get('[data-test="new-discussion-cancel"]').click();

    cy.get('[data-test="new-discussion-input"]').should('not.exist');

    cy.get('[data-test="discussion-post"]').should('have.length', 3);
  });

  it('should publish a new post to the discussion section then proceed to delete it successfully', () => {
    cy.get('#Discussion').should('exist');

    cy.get('[data-test="new-discussion-button"]').click();

    cy.get('[data-test="new-discussion-input"]').type('System Test Text');
    cy.get('[data-test="new-discussion-publish"]').click();

    cy.get('[data-test="discussion-post"]').should('have.length', 4);

    cy.get('[data-test="discussion-post"]')
        .eq(3)
        .find('[data-test="discussion-post-header"]')
        .find('[data-test="discussion-post-context-menu"]')
        .click({force: true});

    cy.get('[data-test="discussion-post"]')
        .find('.grey-rounded-menu > :nth-child(2)')
        .contains('Delete')
        .click({force:true});

    cy.get('[data-test="notification-dialog"]').find('[data-test="confirm-button"]').contains('Delete').click();

    cy.get('[data-test="discussion-post"]').should('have.length', 3);
  });

  it('should publish a new post to the discussion section, delete the post, and cancel the deletion', () => {
    cy.get('#Discussion').should('exist');

    cy.get('[data-test="new-discussion-button"]').click();

    cy.get('[data-test="new-discussion-input"]').type('System Test Text');
    cy.get('[data-test="new-discussion-publish"]').click();

    cy.get('[data-test="discussion-post"]').should('have.length', 4);

    cy.get('[data-test="discussion-post"]')
        .eq(3)
        .find('[data-test="discussion-post-header"]')
        .find('[data-test="discussion-post-context-menu"]')
        .click({force: true});

    cy.get('[data-test="discussion-post"]')
        .find('.grey-rounded-menu > :nth-child(2)')
        .contains('Delete')
        .click({force: true});


    cy.get('[data-test="notification-dialog"]').find('[data-test="cancel-button"]').contains('Cancel').click();

    cy.get('[data-test="discussion-post"]').should('have.length', 4);
  });

  it('Should proceed to edit an existing discussion post and save it', () => {
    cy.get('[data-test="new-discussion-button"').click();

    cy.get('[data-test="new-discussion-input"]').type('System Test Text');
    cy.get('[data-test="new-discussion-publish"]').click();

    cy.get('[data-test="discussion-post"]').should('have.length', 4);

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

  it('Should proceed to edit a discussion post and then cancel it leaving the original post intact', () => {
    cy.get('[data-test="new-discussion-button"').click();

    cy.get('[data-test="new-discussion-input"]').type('System Test Text.');
    cy.get('[data-test="new-discussion-publish"]').click();

    cy.get('[data-test="discussion-post"]').should('have.length', 4);

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

    cy.get('[data-test="discussion-post"]')
        .eq(3)
        .find('[data-test="discussion-post-content"]')
        .should('have.text', 'System Test Text.');
  });
});
