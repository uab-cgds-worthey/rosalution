describe('view_collapsible_case_information.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.visit('/');
    cy.get('.analysis-card').first().click();
  });

  it('can view the case information when expanded and not when its collapsed', () => {
    cy.get('#Brief > div > [data-test="Nominator"] > .section-content').should('be.visible');
    cy.get('#Brief > div > [data-test="Participant"] > .section-content').should('be.visible');
    cy.get('#Clinical_History > div > [data-test="Testing"] > .section-content').should('be.visible');

    cy.get('[data-test="collapsable-icon-Brief"]').click({force: true});
    cy.get('[data-test="collapsable-icon-Clinical History"]').click({force: true});

    cy.get('#Brief > div > [data-test="Nominator"] > .section-content').should('not.be.visible');
    cy.get('#Brief > div > [data-test="Participant"] > .section-content').should('not.be.visible');

    cy.get('#Clinical_History > div > [data-test="Testing"] > .section-content').should('not.be.visible');
  });
});
