describe('view_collapsible_case_information.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.visit('/');
    cy.get('.analysis-card').first().click();
  });

  it('can view the case information when expanded and not when its collapsed', () => {
    cy.get('#Brief > tbody > :nth-child(4) > :nth-child(1) > .field').should('be.visible');
    cy.get('#Brief > tbody > :nth-child(5) > .values > [data-test="value-row"]').should('be.visible');
    cy.get('#Clinical_History > tbody > :nth-child(4) > :nth-child(1) > .field').should('be.visible');
    cy.get(':nth-child(10) > .values > :nth-child(3)').should('be.visible');
    cy.get('#Brief > tbody > .section-header > .section-header-content > .collapsable-logo > .svg-inline--fa').click();
    cy.get(
        '#Clinical_History > tbody > .section-header > .section-header-content > .collapsable-logo > .svg-inline--fa')
        .click();
    cy.get('#Brief > tbody > :nth-child(4) > :nth-child(1) > .field').should('not.be.visible');
    cy.get('#Brief > tbody > :nth-child(5) > .values > [data-test="value-row"]').should('not.be.visible');
    cy.get('#Clinical_History > tbody > :nth-child(4) > :nth-child(1) > .field').should('not.be.visible');
    cy.get(':nth-child(10) > .values > :nth-child(3)').should('not.be.visible');
  });
});
