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
        .invoke('attr', 'style', 'display: block; visibility: visible; opacity: 1;')
        .as('openActionMenu')

    // Adding First Linked Omic Unit
    cy.get('@openActionMenu').within(() => { cy.contains('Add Unit').click() }).invoke('hide');

    cy.get('[data-test="gene-symbol-input"]').type('G6PD')
    cy.get('[data-test="refseq-transcript-input"]').type('NM_001360016.2')
    cy.get('[data-test="hgvs-cdna-input"]').type('c.563C>T')
    cy.get('[data-test="hgvs-protein-input"]').type('p.Ser188Phe')
    cy.get('[data-test="reason-of-interest-input"]').type('Interested in manually adding new omic unit')
    
    cy.get('.primary-button').contains('Add').click();
    cy.get('[data-test="header-title-text"]').click();

    cy.get('[data-test="G6PD-variant-0"]').as('variantRowG6PD')
    
    cy.get('@variantRowG6PD').find('.variant-name-row > .variant-name-line')
        .should('have.text', 'NM_001360016.2:c.563C>T(p.Ser188Phe)')

    // // Editing First Linked Omic Unit, Must enable Edit Mode to Make omic unit editable
    cy.get('@openActionMenu').within(() => { cy.contains('Edit').click() }).invoke('hide');

    cy.get('@variantRowG6PD').should('have.class', 'editable');
    cy.get('@variantRowG6PD').find('[data-test="edit-button"]').click();
    cy.get('[data-test="reason-of-interest-input"]').clear().type('Editing the omic unit of interest')
    cy.get('.primary-button').contains('Edit').click();

    cy.get('@variantRowG6PD').find('.variant-case-information')
        .should('contain.text', 'Editing the omic unit of interest')

    // // Adding Second Linked Omic Unit
    cy.get('@openActionMenu').within(() => { cy.contains('Add Unit').click() }).invoke('hide');

    cy.get('[data-test="gene-symbol-input"]').type('JAK2')
    cy.get('[data-test="refseq-transcript-input"]').type('NM_004972.3')
    cy.get('[data-test="hgvs-cdna-input"]').type('c.1694G>C')
    cy.get('[data-test="hgvs-protein-input"]').type('p.Arg565Thr')
    cy.get('[data-test="reason-of-interest-input"]').type('Second linked omic unit to this other gene')

    cy.get('.primary-button').contains('Add').click();
    cy.get('[data-test="header-title-text"]').click();

    cy.get('[data-test="JAK2-variant-0"]').as('variantRowJAK2')
    cy.get('@variantRowJAK2').find('.variant-name-row > .variant-name-line')
        .should('have.text', 'NM_004972.3:c.1694G>C(p.Arg565Thr)')
    
    // Editing the first linked omic unit again
    cy.get('@variantRowG6PD').should('have.class', 'editable');
    cy.get('@variantRowG6PD').find('[data-test="edit-button"]').click();
    cy.get('[data-test="reason-of-interest-input"]').clear().type('Unicorns really eat rainbows.')
    cy.get('.primary-button').contains('Edit').click();
    cy.get('@variantRowG6PD').find('.variant-case-information')
        .should('contain.text', 'Unicorns really eat rainbows.')

    // Editing the 2nd linked omic unit again
    cy.get('@variantRowJAK2').should('have.class', 'editable');
    cy.get('@variantRowJAK2').find('[data-test="edit-button"]').click();
    cy.get('[data-test="reason-of-interest-input"]').clear().type('Its import to link this one and edit the second one only now.')
    cy.get('.primary-button').contains('Edit').click();
    cy.get('@variantRowJAK2').find('.variant-case-information')
        .should('contain.text', 'Its import to link this one and edit the second one only now.')
  });
});
