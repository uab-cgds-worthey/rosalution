describe('attach_pedigree_image', () => {
  beforeEach(() => {
    cy.resetDatabase();
  });
  it('should attach a jpg pedigree image', () => {
    cy.visit('/login');
    cy.get('[data-test="username-input"]').type('user01');
    cy.get('[data-test="local-login-button"]').click();
    cy.get('[href="/rosalution/analysis/CPAM0002"]').click();
    cy.get('[href="#Pedigree"]').click();
    cy.get('.attach-logo').click();
    cy.get('.drop-file-box-content').selectFile('../backend/tests/fixtures/pedigree-fake.jpg', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();
    cy.get('#Pedigree > tbody > .section-image').should('exist');
  });

  it('should attach a png pedigree image', () => {
    cy.visit('/login');
    cy.get('[data-test="username-input"]').type('user01');
    cy.get('[data-test="local-login-button"]').click();
    cy.get('[href="/rosalution/analysis/CPAM0002"]').click();
    cy.get('[href="#Pedigree"]').click();
    cy.get('.attach-logo').click();
    cy.get('.drop-file-box-content').selectFile('../frontend/src/assets/gnomad-logo.png', {
      action: 'drag-drop',
    });
    cy.get('[data-test="confirm"]').click();
    cy.get('#Pedigree > tbody > .section-image').should('exist');
  });
});
