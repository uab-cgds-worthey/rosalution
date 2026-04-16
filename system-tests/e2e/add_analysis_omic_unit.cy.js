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
        .as('openActionMenu');

    // Adding First Manual Omic Unit
    cy.get('@openActionMenu').contains('Add Unit').click();
    cy.get('@openActionMenu').invoke('hide');

    cy.get('[data-test="gene-symbol-input"]').type('G6PD');
    cy.get('[data-test="refseq-transcript-input"]').type('NM_001360016.2');
    cy.get('[data-test="hgvs-cdna-input"]').type('c.563C>T');
    cy.get('[data-test="hgvs-protein-input"]').type('p.Ser188Phe');
    cy.get('[data-test="reason-of-interest-input"]').type('Interested in manually adding new omic unit');

    cy.get('.primary-button').contains('Add').click();
    cy.get('[data-test="header-title-text"]').click();

    cy.get('[data-test="G6PD-variant-0"]').as('variantRowG6PD');

    cy.get('@variantRowG6PD').find('.variant-name-row > .variant-name-line')
        .should('have.text', 'NM_001360016.2:c.563C>T(p.Ser188Phe)');

    // Editing First Manual Omic Unit, Must enable Edit Mode to Make omic unit editable
    cy.get('@openActionMenu').contains('Add Unit').click();
    cy.get('@openActionMenu').invoke('hide'); ;

    cy.get('@variantRowG6PD').should('have.class', 'editable');
    cy.get('@variantRowG6PD').find('[data-test="edit-button"]').click();
    cy.get('[data-test="reason-of-interest-input"]').clear();
    cy.get('[data-test="reason-of-interest-input"]').type('Editing the omic unit of interest');
    cy.get('.primary-button').contains('Edit').click();

    cy.get('@variantRowG6PD').find('.variant-case-information')
        .should('contain.text', 'Editing the omic unit of interest');

    // Making sure the system will not add an existing variant
    cy.get('@openActionMenu').contains('Add Unit').click();
    cy.get('@openActionMenu').invoke('hide');

    cy.get('[data-test="gene-symbol-input"]').type('G6PD');
    cy.get('[data-test="refseq-transcript-input"]').type('NM_001360016.2');
    cy.get('[data-test="hgvs-cdna-input"]').type('c.563C>T');
    cy.get('[data-test="hgvs-protein-input"]').type('p.Ser188Phe');
    cy.get('[data-test="reason-of-interest-input"]').type('Interested in manually adding new omic unit');

    cy.get('.primary-button').contains('Add').click();
    cy.get('[data-test="header-title-text"]').click();

    cy.get('[data-test^="G6PD-variant"]').should('have.length', 1);

    // // Adding Second Manual Omic Unit
    cy.get('@openActionMenu').contains('Add Unit').click();
    cy.get('@openActionMenu').invoke('hide');

    cy.get('[data-test="gene-symbol-input"]').type('JAK2');
    cy.get('[data-test="refseq-transcript-input"]').type('NM_004972.3');
    cy.get('[data-test="hgvs-cdna-input"]').type('c.1694G>C');
    cy.get('[data-test="hgvs-protein-input"]').type('p.Arg565Thr');
    cy.get('[data-test="reason-of-interest-input"]').type('Second linked omic unit to this other gene');

    cy.get('.primary-button').contains('Add').click();
    cy.get('[data-test="header-title-text"]').click();

    cy.get('[data-test="JAK2-variant-0"]').as('variantRowJAK2');
    cy.get('@variantRowJAK2').find('.variant-name-row > .variant-name-line')
        .should('have.text', 'NM_004972.3:c.1694G>C(p.Arg565Thr)');

    // Editing the first manual omic unit again
    cy.get('@variantRowG6PD').should('have.class', 'editable');
    cy.get('@variantRowG6PD').find('[data-test="edit-button"]').click();
    cy.get('[data-test="reason-of-interest-input"]').clear();
    cy.get('[data-test="reason-of-interest-input"]').type('Unicorns really eat rainbows.');
    cy.get('.primary-button').contains('Edit').click();
    cy.get('@variantRowG6PD').find('.variant-case-information')
        .should('contain.text', 'Unicorns really eat rainbows.');

    // Editing the 2nd manual omic unit again
    cy.get('@variantRowJAK2').should('have.class', 'editable');
    cy.get('@variantRowJAK2').find('[data-test="edit-button"]').click();
    cy.get('[data-test="reason-of-interest-input"]').clear();
    cy.get('[data-test="reason-of-interest-input"]')
        .type('Its import to link this one and edit the second one only now.');
    cy.get('.primary-button').contains('Edit').click();
    cy.get('@variantRowJAK2').find('.variant-case-information')
        .should('contain.text', 'Its import to link this one and edit the second one only now.');

    // Deleting the first manual omic unit
    cy.get('.gene-box-header').should('have.length', 3);
    cy.get('@variantRowG6PD').should('have.class', 'editable');
    cy.get('@variantRowG6PD').find('[data-test="delete-button"]').click();

    cy.get('[data-test="confirm-button"').contains('Delete').click();
    cy.get('.gene-box-header').should('have.length', 2);

    cy.get('[data-test="gene-name"]')
        .should('have.length', 2)
        .each(($el) => {
          cy.wrap($el).invoke('text').should('not.contain', 'G6PD');
        });

    // Adding third omic unit but to existing manual gene JAK2
    cy.get('@openActionMenu').contains('Add Unit').click();
    cy.get('@openActionMenu').invoke('hide');

    cy.get('[data-test="gene-symbol-input"]').type('JAK2');
    cy.get('[data-test="refseq-transcript-input"]').type('NM_004972.4');
    cy.get('[data-test="hgvs-cdna-input"]').type('c.1849G>A');
    cy.get('[data-test="hgvs-protein-input"]').type('p.Val617Ile');
    cy.get('[data-test="reason-of-interest-input"]').type('Third linked omic unit to second added gene');

    cy.get('.primary-button').contains('Add').click();
    cy.get('[data-test="header-title-text"]').click();

    cy.get('[data-test^="JAK2-variant"]')
        .as('JAK2Variants')
        .should('have.length', 2);
    cy.get('[data-test="JAK2-variant-1"]')
        .as('secondJAK2Variant')
        .find('.variant-name-row > .variant-name-line')
        .should('contain.text', 'NM_004972.4:c.1849G>A(p.Val617Ile)');

    // Editing the first JAK2 variant again and making sure second JAK2 Variant is not affected
    cy.get('@variantRowJAK2').find('[data-test="edit-button"]').click();
    cy.get('[data-test="reason-of-interest-input"]').clear();
    cy.get('[data-test="reason-of-interest-input"]').type('Editing the first JAK2 variant');
    cy.get('.primary-button').contains('Edit').click();
    cy.get('@variantRowJAK2').find('.variant-case-information')
        .should('contain.text', 'Editing the first JAK2 variant');

    cy.get('@secondJAK2Variant').find('.variant-case-information')
        .should('contain.text', 'Third linked omic unit to second added gene');

    // Adding another variant to the original VMA21 gene that isn't a manually added gene
    cy.get('@openActionMenu').contains('Add Unit').click();
    cy.get('@openActionMenu').invoke('hide');

    cy.get('[data-test="gene-symbol-input"]').type('VMA21');
    cy.get('[data-test="refseq-transcript-input"]').type('NM_001017980.4');
    cy.get('[data-test="hgvs-cdna-input"]').type('c.76A>G');
    cy.get('[data-test="hgvs-protein-input"]').type('p.Thr26Ala');
    cy.get('[data-test="reason-of-interest-input"]').type('4th omic unit added to original VMA21 gene');

    cy.get('.primary-button').contains('Add').click();
    cy.get('[data-test="header-title-text"]').click();

    cy.get('[data-test^="VMA21-variant"]')
        .as('VMA21Variants')
        .should('have.length', 2);
    cy.get('[data-test="VMA21-variant-1"]')
        .as('secondVMA21Variant')
        .find('.variant-name-row > .variant-name-line')
        .should('contain.text', 'NM_001017980.4:c.76A>G(p.Thr26Ala)');
    cy.get('[data-test="VMA21-variant-0"]')
        .as('originalVMA21Variant')
        .find('.variant-name-row > .variant-name-line')
        .should('not.have.class', 'editable');
    cy.get('@secondVMA21Variant').should('have.class', 'editable');

    // Deleting the first manual omic unit
    cy.get('.gene-box-header').should('have.length', 2);
    cy.get('@secondVMA21Variant').find('[data-test="delete-button"]').click();

    cy.get('[data-test="confirm-button"').contains('Delete').click();
    cy.get('.gene-box-header').should('have.length', 2);
    cy.get('[data-test^="VMA21-variant"]')
        .as('VMA21Variants')
        .should('have.length', 1);
    cy.get('@originalVMA21Variant')
        .find('.variant-name-row > .variant-name-line')
        .should('not.have.class', 'editable');
  });
});
