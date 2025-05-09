describe('status_filter_case_cards.cy.js', () => {
  before(() => {
    cy.resetDatabase();
  });
  beforeEach(() => {
    cy.visit('/');
    cy.get('.legend > [data-test="Preparation"]').as('PreparationStatus');
    cy.get('.legend > [data-test="Ready"]').as('ReadyStatus');
    cy.get('.legend > [data-test="Active"]').as('ActiveStatus');
    cy.get('.legend > [data-test="Approved"]').as('ApprovedStatus');
    cy.get('.legend > [data-test="On-Hold"]').as('OnHoldStatus');
    cy.get('.legend > [data-test="Declined"]').as('DeclinedStatus');
  });
  it('filters cases by status', () => {
    cy.get('[data-test="analysis-card"]').should('have.length', 6);

    cy.get('@PreparationStatus').click();
    cy.get('[data-test="analysis-card"]')
        .should('have.length', 1)
        .should('contain', 'CPAM0084');

    cy.get('@ReadyStatus').click();
    cy.get('@ActiveStatus').click();
    cy.get('[data-test="analysis-card"]')
        .should('have.length', 2)
        .should('contain', 'CPAM0053');

    cy.get('@ActiveStatus').click();
    cy.get('@ApprovedStatus').click();
    cy.get('[data-test="analysis-card"]').should('have.length', 4);

    cy.get('@ApprovedStatus').click();
    cy.get('@OnHoldStatus').click();
    cy.get('[data-test="analysis-card"]').should('have.length', 2);

    cy.get('@ApprovedStatus').click();
    cy.get('@DeclinedStatus').click();
    cy.get('[data-test="analysis-card"]')
        .should('have.length', 6)
        .should('contain', 'CPAM0002')
        .should('contain', 'CPAM0046');

    cy.get('@ActiveStatus').click();
    cy.get('@DeclinedStatus').click();
    cy.get('[data-test="analysis-card"]')
        .should('have.length', 2)
        .should('contain', 'CPAM0047')
        .should('contain', 'CPAM0065');
    cy.get('@DeclinedStatus').click();
  });

  it('filters cases by multiple statuses', () => {
    cy.get('[data-test="analysis-card"]').should('have.length', 6);
    cy.get('@PreparationStatus').click();
    cy.get('@ReadyStatus').click();
    cy.get('[data-test="analysis-card"]')
        .should('have.length', 2)
        .should('contain', 'CPAM0053')
        .should('contain', 'CPAM0084');
  });

  it('resets the filters if all are selected', () => {
    cy.get('[data-test="analysis-card"]').should('have.length', 6);
    cy.get('@PreparationStatus').click();
    cy.get('[data-test="analysis-card"]').should('have.length', 1);
    cy.get('@ReadyStatus').click();
    cy.get('[data-test="analysis-card"]').should('have.length', 2);
    cy.get('@ActiveStatus').click();
    cy.get('[data-test="analysis-card"]').should('have.length', 2);
    cy.get('@ApprovedStatus').click();
    cy.get('[data-test="analysis-card"]').should('have.length', 4);
    cy.get('@OnHoldStatus').click();
    cy.get('[data-test="analysis-card"]').should('have.length', 4);
    cy.get('@DeclinedStatus').click();
    cy.get('[data-test="analysis-card"]').should('have.length', 6);
    cy.get('.legend > :nth-child(2)').click();
    cy.get('[data-test="analysis-card"]').should('have.length', 1);
  });
});
