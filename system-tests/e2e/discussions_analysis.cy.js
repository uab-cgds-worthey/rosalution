describe('discussions_analysis.cy.js', () => {
    beforeEach(() => {
        cy.resetDatabase();
        cy.visit('/');
        cy.get('.analysis-card').first().click();
        cy.get('[href="#Discussion"]').click();
    });

    it('should publish a new post to the discussion section', () => {
        cy.get('#Discussion').should('exist');

        cy.get('[data-test="new-discussion-button"]').click()

        cy.get('[data-test="discussion-post"]').should('have.length', 3);

        cy.get('[data-test="new-discussion-input"]').type("System Test Text");
        cy.get('[data-test="new-discussion-publish"]').click();

        cy.get('[data-test="discussion-post"]').should('have.length', 4);
    });

    it('should not be able to publish a post with no text in the new discussion field', () => {
        cy.get('#Discussion').should('exist');

        cy.get('[data-test="new-discussion-button"]').click()
        cy.get('[data-test="new-discussion-publish"]').should('be.disabled')
    });

    it('should cancel a new post, close the new post field, and not post anything', () => {
        cy.get('#Discussion').should('exist');

        cy.get('[data-test="new-discussion-button"]').click()

        cy.get('[data-test="new-discussion-input"]').type("System Test Text");
        cy.get('[data-test="new-discussion-cancel"]').click();

        cy.get('[data-test="new-discussion-input"]').should('not.exist');

        cy.get('[data-test="discussion-post"]').should('have.length', 3);
    });
});