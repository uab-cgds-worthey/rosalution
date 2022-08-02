describe('rosalution.cy.js', () => {
  beforeEach(() => {
    cy.resetDatabase();
  });

  it('renders the webpage', () => {
    cy.visit('/');
  });
});
