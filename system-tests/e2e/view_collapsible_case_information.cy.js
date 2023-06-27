describe('view_collapsible_case_information.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.visit('/');
    cy.get('.analysis-card').first().click();
  });

  it('can view the case information when expanded and not when its collapsed', () => {
    // TODO: Come back and fix after the blank line items are visible.
    cy.get('#Brief > div > [data-test="Goals"] > .section-content').should('be.visible');
    cy.get('#Brief > div > [data-test="Proposed Model/Project"] > .section-content').should('be.visible');
    cy.get('#Clinical_History > div > [data-test="Testing"] > .section-content').should('be.visible');
    cy.get(':nth-child(10) > .values > :nth-child(3)').should('be.visible');
    
    cy.get('#Brief > div > .rosalution-section-header > .rosalution-header-right-icons > .collapsable-logo > .svg-inline--fa').click();
    cy.get(
        '#Clinical_History > div > .rosalution-section-header > .rosalution-header-right-icons > .collapsable-logo > .svg-inline--fa')
        .click();

    
    cy.get('#Brief > div > [data-test="Goals"] > .section-content').should('not.be.visible');
    cy.get('#Brief > div > [data-test="Proposed Model/Project"] > .section-content').should('not.be.visible');
    
    cy.get('#Clinical_History > div > [data-test="Testing"] > .section-content').should('not.be.visible');
  });
});
