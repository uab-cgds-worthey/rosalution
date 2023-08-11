describe('upload_images_to_case_annotations.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.visit('/analysis/CPAM0047/annotation/');
  });

  it('unable to upload for a user without permissions', () => {
    cy.login('user03');
    cy.visit('/analysis/CPAM0047/annotation/');
    cy.get('[href="#Gene_Homology"]').click();
    cy.get('[data-test="Gene Homology/Multi-Sequence Alignment"]').should('not.have.descendants', 'button');
  });

  it('uploads an image to the gene homology section', () => {
    cy.get('[href="#Gene_Homology"]').click();
    cy.get('#Gene_Homology > .rosalution-section-header > [data-test="attach-logo"]').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/pedigree-fake.jpg', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();
    cy.get('[data-test="annotation-image"]').should('exist');
  });

  it('uploads two images to the gene homology section', () => {
    // First Image
    cy.get('[href="#Gene_Homology"]').click();
    cy.get('#Gene_Homology > .rosalution-section-header > [data-test="attach-logo"]').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/pedigree-fake.jpg', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();

    // Second Image
    cy.get('[href="#Gene_Homology"]').click();
    cy.get('#Gene_Homology > .rosalution-section-header > [data-test="attach-logo"]').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/pedigree-fake-2.jpg', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();

    cy.get('[data-test="annotation-image"]').should('have.length', 2);
  });

  it('uploads an image to the protein expression section and then updates the image with a different image', () => {
    cy.get('[href="#Modelability"]').click();
    cy.get('#Modelability > .rosalution-section-header > [data-test="attach-logo"]').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/pedigree-fake.jpg', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();

    cy.get('[data-test=annotation-edit-icon]').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/pedigree-fake-2.jpg', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"').click();
    cy.get('[data-test="annotation-image"]').should('exist');
    cy.get('[data-test="annotation-image"]').should('have.length', 1);
  });

  it('uploads an image to the Druggability section and then removes the image', () => {
    cy.get('[href="#Druggability"]').click();
    cy.get('#Druggability > .rosalution-section-header > [data-test="attach-logo"]').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/pedigree-fake.jpg', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();

    cy.get('[data-test=annotation-edit-icon]').click();
    cy.get('[data-test="delete"]').click();
    cy.get('[data-test="confirm-button"').click();
    cy.get('[data-test="annotation-image"]').should('not.exist');
  });
});
