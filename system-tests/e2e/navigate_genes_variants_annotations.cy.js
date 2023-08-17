describe('drop_down_menu_genes_variants.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.visit('/');
    cy.get('[href="/rosalution/analysis/CPAM0047"]').click();
  });

  it('selects a variant in an analysis to view annotations and navigate to other genes and variants in case', () => {
    cy.get('[data-test="variant-route-1"]').click();
    cy.get('.gene-unit-select').should('exist');
    cy.get('.gene-unit-select').should('contain', 'SBF1');
    cy.get('.variant-unit-select').should('exist');
    cy.get('.variant-unit-select option:selected')
        .invoke('text').should('eq', 'NM_002972.2:c.5474_5475delTG(Val1825GlyfsX27)');

    cy.get('#Gene > .rosalution-section-header > .rosalution-section-header-text')
        .should('contain', 'SBF1');
    cy.get('#Variant > .rosalution-section-header > .rosalution-section-header-text')
        .should('contain', 'NM_002972.2:c.5474_5475delTG(Val1825GlyfsX27)');

    cy.get('.variant-unit-select').select('NM_002972.2:c.3493_3494dupTA(Pro1166ThrfsX5)');

    cy.get('#Variant > .rosalution-section-header > .rosalution-section-header-text')
        .should('contain', 'NM_002972.2:c.3493_3494dupTA(Pro1166ThrfsX5)');
    cy.get('#Variant > .rosalution-section-header > .rosalution-section-header-text')
        .should('not.contain', 'NM_002972.2:c.5474_5475delTG(Val1825GlyfsX27)');

    cy.get('.variant-unit-select').select('NM_002972.2:c.5474_5475delTG(Val1825GlyfsX27)');
    cy.get('#Variant > .rosalution-section-header > .rosalution-section-header-text')
        .should('contain', 'NM_002972.2:c.5474_5475delTG(Val1825GlyfsX27)');
    cy.get('#Variant > .rosalution-section-header > .rosalution-section-header-text')
        .should('not.contain', 'NM_002972.2:c.3493_3494dupTA(Pro1166ThrfsX5)');
  });
});
