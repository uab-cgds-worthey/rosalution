describe('upload_images_to_case_annotations.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.fixture('section-image-1.jpg', {encoding: null}).as('sectionImage1');
    cy.fixture('section-image-2.png', {encoding: null}).as('sectionImage2');
    cy.intercept('/rosalution/api/analysis/CPAM0047/summary').as('analysisSummaryLoad');

  });

  it('manages successully and failed attempts to upload images for users', () => {
    // Test Being Unable to Attach Image without Permissions
    cy.login('researcher');
    cy.visit('/analysis/CPAM0047/annotation/');
    cy.wait('@analysisSummaryLoad');
    cy.get('[href="/rosalution/analysis/CPAM0047/annotation#Gene_Homology"]').click();
    cy.get('[data-test="Gene Homology/Multi-Sequence Alignment"]').should('not.have.descendants', 'button');

    // Test uploading a single image
    cy.login('vrr-prep')
    cy.visit('/analysis/CPAM0047/annotation/');
    cy.wait('@analysisSummaryLoad');
    cy.get('[href="/rosalution/analysis/CPAM0047/annotation#Gene_Homology"]').click();
    cy.get('#Gene_Homology > .rosalution-section-header > [data-test="attach-logo"]').click();
    cy.get('.drop-file-box-content').selectFile('@sectionImage1', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();
    cy.get('[data-test="annotation-image"]').should('exist');

    // Test uploading a second image to the same section
    cy.get('[href="/rosalution/analysis/CPAM0047/annotation#Gene_Homology"]').click();
    cy.get('#Gene_Homology > .rosalution-section-header > [data-test="attach-logo"]').click();
    cy.get('.drop-file-box-content').selectFile('@sectionImage1', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();

    cy.get('[data-test="annotation-image"]').should('have.length', 2);

    // Test Editing an Image
    cy.get('[href="/rosalution/analysis/CPAM0047/annotation#Modelability"]').click();
    cy.get('#Modelability > .rosalution-section-header > [data-test="attach-logo"]').click();
    cy.get('.drop-file-box-content').selectFile('@sectionImage1', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();

    cy.get('#Modelability [data-test="annotation-image"]').then(($annotationImage) => {
      const firstId = $annotationImage.attr('id');

      cy.get('#Modelability [data-test=annotation-edit-icon]').click();
      cy.get('.drop-file-box-content').selectFile('@sectionImage2', {
        action: 'drag-drop',
      });
      cy.get('[data-test="confirm"').click();

      cy.get('#Modelability [data-test="annotation-image"]').invoke('attr', 'id').should('not.eq', firstId);
    });

    // Testing Removing an Image
    cy.get('[href="/rosalution/analysis/CPAM0047/annotation#Druggability"]').click();
    cy.get('#Druggability > .rosalution-section-header > [data-test="attach-logo"]').click();
    cy.get('.drop-file-box-content').selectFile('@sectionImage1', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();

    cy.get('#Druggability [data-test=annotation-edit-icon]').click();
    cy.get('[data-test="delete"]').click();
    cy.get('[data-test="confirm-button"').click();
    cy.get('#Druggability [data-test="annotation-image"]').should('not.exist');
  });
});
