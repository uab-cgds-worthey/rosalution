describe('attach analysis section images', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.fixture('section-image-1.jpg', {encoding: null}).as('sectionImage1');
    cy.fixture('section-image-2.png', {encoding: null}).as('sectionImage2');
    cy.login('vrr-prep');
    cy.visit('/');
    cy.get('[href="/rosalution/analysis/CPAM0002"]').click();
  });

  it('should attach a jpg pedigree image', () => {
    cy.get('[href="#Pedigree"]').click();
    cy.get('[data-test="attach-logo-Pedigree"]').click({force: true});
    cy.get('.drop-file-box-content').selectFile('@sectionImage1', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();

    cy.get('[field="Pedigree"] > .image-row').should('exist');
  });

  it('should attach a png pedigree image', () => {
    cy.get('[href="#Pedigree"]').click();
    cy.get('[data-test="attach-logo-Pedigree"]').click({force: true});
    cy.get('.drop-file-box-content').selectFile('@sectionImage2', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();

    cy.get('[field="Pedigree"] > .image-row').should('exist');
  });

  it('should attach two images to the pedigree section', () => {
    // First image - jpg
    cy.get('[href="#Pedigree"]').click();
    cy.get('[data-test="attach-logo-Pedigree"]').click({force: true});
    cy.get('.drop-file-box-content').selectFile('@sectionImage1', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();

    // Second image - png
    cy.get('[href="#Pedigree"]').click();
    cy.get('[data-test="attach-logo-Pedigree"]').click({force: true});
    cy.get('.drop-file-box-content').selectFile('@sectionImage2', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();

    cy.get('[field="Pedigree"] > .image-row').should('have.length', 2);
  });

  it('should attach an image and then updates the image to another image ', () => {
    cy.get('[href="#Pedigree"]').click();
    cy.get('[data-test="attach-logo-Pedigree"]').click({force: true});
    cy.get('.drop-file-box-content').selectFile('@sectionImage1', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();

    cy.get('[field="Pedigree"] > .image-row > a').invoke('attr', 'href').then((oldFileUrl) => {
      cy.get('[data-test=annotation-edit-icon]').click({force: true});
      cy.get('.drop-file-box-content').selectFile('@sectionImage2', {
        action: 'drag-drop',
      });
      cy.get('[data-test="confirm"]').click();

      cy.get('[field="Pedigree"] > .image-row > a').invoke('attr', 'href').should('not.contain', oldFileUrl);
    });
  });

  it('should upload an image to Pedigree and then remove the image', () => {
    cy.get('[href="#Pedigree"]').click();
    cy.get('[data-test="attach-logo-Pedigree"]').click({force: true});
    cy.get('.drop-file-box-content').selectFile('@sectionImage1', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();

    cy.get('[data-test=annotation-edit-icon]').click({force: true});
    cy.get('[data-test="delete"]').click();
    cy.get('[data-test="confirm-button"').click();

    cy.get('[field="Pedigree"] > .image-row').should('not.exist');
  });
});
