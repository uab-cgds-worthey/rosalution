describe('upload_images_to_case_annotations.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.visit('/');
    cy.get('[href="/rosalution/analysis/CPAM0047"]').click();
    cy.get('[data-test="gene-name"]').click();
  });

  it('uploads an image to the gene homology section', () => {
    cy.get('[href="#Gene_Homology"]').click();
    cy.get('#Gene_Homology > tbody > .section-header > [data-test="attach-logo"]').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/pedigree-fake.jpg', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();
    cy.get('#Gene_Homology > tbody > .annotation-image').should('exist');
  });

  it('uploads an image to the protein expression section', () => {
    cy.get('[href="#Protein_Expression"]').click();
    cy.get('#Protein_Expression > tbody > .section-header > [data-test="attach-logo"]').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/pedigree-fake.jpg', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();
    cy.get('#Protein_Expression > tbody > .annotation-image').should('exist');
  });

  it('uploads an image to the modelability section', () => {
    cy.get('[href="#Modelability"]').click();
    cy.get('#Modelability > tbody > .section-header > [data-test="attach-logo"]').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/pedigree-fake.jpg', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();
    cy.get('#Modelability > tbody > .annotation-image').should('exist');
  });
});
