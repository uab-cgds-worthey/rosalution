describe('edit_case_analysis.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.visit('/login');
    cy.get('[data-test="username-input"]').type('user01');
    cy.get('[data-test="local-login-button"]').click();
    cy.get('.analysis-card').first().click();
    cy.get('.grey-rounded-menu').invoke('attr', 'style', 'display: block; visibility: visible; opacity: 1;');
    cy.get('[data-test="user-menu"] > .grey-rounded-menu > :nth-child(1)').contains('Edit').click();
    cy.get('.grey-rounded-menu').invoke('attr', 'style', 'display: block; visibility: hidden; opacity: 0;');
  });

  it('Enables editing an analysis', () => {
    cy.get('#Brief > tbody > :nth-child(5) > .values > [data-test="editable-value"]').should('exist');
    cy.get('[data-test="save-edit-button"]').should('exist');
  });

  it('edits a value & saves to the analysis', () => {
    cy.get('#Brief > tbody > :nth-child(5) > .values > [data-test="editable-value"]').click();
    cy.get('#Brief > tbody > :nth-child(5) > .values > [data-test="editable-value"]').type('test');
    cy.get('#Brief > tbody > :nth-child(5) > .values > [data-test="editable-value"]').should('contain', 'test');
    cy.get('[data-test="save-edit-button"]').should('exist');
    cy.get('[data-test="save-edit-button"]').click();
    cy.get('[data-test="save-edit-button"]').should('not.exist');
    cy.get('.rosalution-logo').click();
    cy.get('.analysis-card').first().click();
    cy.get(':nth-child(6) > .values > [data-test="value-row"]').should('contain', 'test');
    cy.get('#Brief > tbody > :nth-child(4) > .values > [data-test="value-row"]')
        .should('contain', 'Dr. Person One');
  });
});
