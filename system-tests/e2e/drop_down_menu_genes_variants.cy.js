describe('drop_down_menu_genes_variants.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.visit('/login');
    cy.get('[data-test="username-input"]').type('user01');
    cy.get('[data-test="local-login-button"]').click();
    cy.get('[href="/rosalution/analysis/CPAM0047"]').click();
    cy.get('[data-test="gene-name"]').click();
  });

  it('has a drop-down menu for the gene', () => {
    cy.get('.gene-unit-select').should('exist');
    cy.get('.gene-unit-select').should('contain', 'SBF1');
    cy.get('.gene-unit-select').select('SBF1');
    cy.get('.gene-unit-select').should('contain', 'SBF1');
  });

  it('has a drop-down menu for the variant and navigates to the proper variants', () => {
    cy.get('.variant-unit-select').should('exist');
    cy.get('.variant-unit-select').should('contain', 'NM_002972.2:c.3493_3494dupTA(Pro1166ThrfsX5)');
    cy.get('.variant-unit-select').select('NM_002972.2:c.3493_3494dupTA(Pro1166ThrfsX5)');
    cy.get('#Variant > tbody > .section-header > :nth-child(1) > .section-name')
        .should('contain', 'NM_002972.2:c.3493_3494dupTA(Pro1166ThrfsX5)');
    cy.get('#Variant > tbody > .section-header > :nth-child(1) > .section-name')
        .should('not.contain', 'NM_002972.2:c.5474_5475delTG(Val1825GlyfsX27)');

    cy.get('.variant-unit-select').select('NM_002972.2:c.5474_5475delTG(Val1825GlyfsX27)');
    cy.get('#Variant > tbody > .section-header > :nth-child(1) > .section-name')
        .should('contain', 'NM_002972.2:c.5474_5475delTG(Val1825GlyfsX27)');
    cy.get('#Variant > tbody > .section-header > :nth-child(1) > .section-name')
        .should('not.contain', 'NM_002972.2:c.3493_3494dupTA(Pro1166ThrfsX5)');
  });
});
