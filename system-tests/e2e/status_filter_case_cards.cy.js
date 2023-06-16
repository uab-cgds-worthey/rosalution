describe('status_filter_case_cards.cy.js', () => {
  before(() => {
    cy.resetDatabase();
  });
  beforeEach(() => {
    cy.visit('/');
  });

  it('filters cases by status', () => {
    cy.get('.analysis-card').should('have.length', 6);
    cy.get('.legend > :nth-child(1)').click();
    cy.get('.analysis-card').should('have.length', 1);
    cy.get('.case-name').should('contain', 'CPAM0084');
    cy.get('.legend > :nth-child(1)').click();
    cy.get('.legend > :nth-child(2)').click();
    cy.get('.analysis-card').should('have.length', 1);
    cy.get('.case-name').should('contain', 'CPAM0053');
    cy.get('.legend > :nth-child(2)').click();
    cy.get('.legend > :nth-child(3)').click();
    cy.get('.analysis-card').should('have.length', 0);
    cy.get('.legend > :nth-child(3)').click();
    cy.get('.legend > :nth-child(4)').click();
    cy.get('.analysis-card').should('have.length', 0);
    cy.get('.legend > :nth-child(4)').click();
    cy.get('.legend > :nth-child(5)').click();
    cy.get('.analysis-card').should('have.length', 2);
    cy.get('.analysis-card > .analysis-base').should('contain', 'CPAM0002');
    cy.get('.analysis-card > .analysis-base').should('contain', 'CPAM0046');
    cy.get('.legend > :nth-child(5)').click();
    cy.get('.legend > :nth-child(6)').click();
    cy.get('.analysis-card').should('have.length', 2);
    cy.get('.analysis-card > .analysis-base').should('contain', 'CPAM0047');
    cy.get('.analysis-card > .analysis-base').should('contain', 'CPAM0065');
    cy.get('.legend > :nth-child(6)').click();
  });

  it('filters cases by multiple statuses', () => {
    cy.get('.analysis-card').should('have.length', 6);
    cy.get('.legend > :nth-child(1)').click();
    cy.get('.legend > :nth-child(2)').click();
    cy.get('.analysis-card').should('have.length', 2);
    cy.get('.analysis-card > .analysis-base').should('contain', 'CPAM0053');
    cy.get('.analysis-card > .analysis-base').should('contain', 'CPAM0084');
  });

  it('resets the filters if all are selected', () => {
    cy.get('.analysis-card').should('have.length', 6);
    cy.get('.legend > :nth-child(1)').click();
    cy.get('.analysis-card').should('have.length', 1);
    cy.get('.legend > :nth-child(2)').click();
    cy.get('.analysis-card').should('have.length', 2);
    cy.get('.legend > :nth-child(3)').click();
    cy.get('.analysis-card').should('have.length', 2);
    cy.get('.legend > :nth-child(4)').click();
    cy.get('.analysis-card').should('have.length', 2);
    cy.get('.legend > :nth-child(5)').click();
    cy.get('.analysis-card').should('have.length', 4);
    cy.get('.legend > :nth-child(6)').click();
    cy.get('.analysis-card').should('have.length', 6);
    cy.get('.legend > :nth-child(2)').click();
    cy.get('.analysis-card').should('have.length', 1);
  });
});