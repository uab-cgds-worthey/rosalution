(Cypress.config('isInteractive') ? describe : describe.skip)('edit_case_analysis.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.intercept('/rosalution/api/analysis/CPAM0002').as('analysisLoad');
    cy.visit('analysis/CPAM0002');
    cy.wait('@analysisLoad');
  });

  it('adds, edits, and removes new omic units to an analysis', () => {
    cy.get('[data-test="user-menu"]')
        .find('.grey-rounded-menu')
        .as('userActionMenu')
        .invoke('attr', 'style', 'display: block; visibility: visible; opacity: 1;');
    cy.get('@userActionMenu').contains('Add Unit').click();
    // cy.get('@userActionMenu').invoke('attr', 'style', 'display: block; visibility: hidden; opacity: 0;');

    //     # new_genomic_unit_dict = {
    // #     'transcript': "NM_004972.3",
    // #     'gene': "JAK2",
    // #     'cdna': "c.1694G>C",
    // #     'protein': "p.Arg565Thr",
    // #     'reason_of_interest': "Find this variant interesting to explore.",
    // # }

    // cy.intercept('/rosalution/api/analysis/CPAM0002/genomic_unit').as('omicUnitChange');

    cy.get('[data-test="gene-symbol-input"]').type('G6PD')
    cy.get('[data-test="refseq-transcript-input"]').type('NM_001360016.2')
    cy.get('[data-test="hgvs-cdna-input"]').type('c.563C>T')
    cy.get('[data-test="hgvs-protein-input"]').type('p.Ser188Phe')
    cy.get('[data-test="reason-of-interest-input"]').type('Interested in manually adding new omic unit')
    
    cy.get('.primary-button').contains('Add').click();
    // cy.wait('@omicUnitChange')
    cy.get('[data-test="header-title-text"]').click();

    cy.get('[data-test="G6PD-variant-0"]').as('variantRowG6PD')
    
    cy.get('@variantRowG6PD').find('.variant-name-row > .variant-name-line')
        .should('have.text', 'NM_001360016.2:c.563C>T(p.Ser188Phe)')

    cy.get('@userActionMenu').contains('Edit').click();
    cy.get('@userActionMenu').invoke('attr', 'style', 'display: block; visibility: hidden; opacity: 0;');

    cy.get('@variantRowG6PD').should('have.class', 'editable');
    cy.get('@variantRowG6PD').find('[data-test="edit-button"]').click();

    cy.get('[data-test="reason-of-interest-input"]').type('Editing the omic unit of interest')
    cy.get('.primary-button').contains('Edit').click();

    cy.get('@variantRowG6PD').find('.variant-case-information')
        .should('have.text', 'Editing the omic unit of interest')

    // cy.get('[data-test="user-menu"]')
    //     .find('.grey-rounded-menu')
    //     .as('userActionMenu')
    //     .invoke('attr', 'style', 'display: block; visibility: visible; opacity: 1;');
    // cy.get('@userActionMenu').contains('Edit').click();
    // cy.get('@userActionMenu').invoke('attr', 'style', 'display: block; visibility: hidden; opacity: 0;');

    // cy.get('[href="#Brief"]').click();
    // cy.get('#Brief > div > [data-test="Phenotype"] > .section-content > [data-test="editable-value"]')
    //     .as('editablePhenotype')
    //     .click();
    // cy.get('@editablePhenotype').type('test');
    // cy.get('@editablePhenotype').should('contain', 'test');

    // // Save the changes to persist the analysis
    // cy.get('[data-test="save-edit-button"]').should('exist');
    // cy.get('[data-test="save-edit-button"]').click();
    // cy.get('[data-test="save-edit-button"]').should('not.exist');

    // // Verify that the changes persist once the save is complete
    // cy.get('[href="#Brief"]').click();
    // cy.get('#Brief > div > [data-test="Phenotype"] > .section-content').as('phenotypeField').should('contain', 'test');

    // // Visit CPAM0046 analysis to verify the updated field in CPAM0002 does not appear
    // cy.visit('analysis/CPAM0046');
    // cy.wait('@analysisLoad');
    // cy.get('[href="#Brief"]').click();
    // cy.get('@phenotypeField').contains('test').should('not.exist');

    // // Return to CPAM0002 analysis and verify the updated field is persisted
    // cy.visit('analysis/CPAM0002');
    // cy.wait('@analysisLoad');
    // cy.get('[href="#Brief"]').click();
    // cy.get('@phenotypeField').contains('test').should('exist');
  });
});
