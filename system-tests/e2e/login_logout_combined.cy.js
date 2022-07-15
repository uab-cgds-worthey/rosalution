describe('login_logout_combined.cy.js', () => {
  it('app url redirects to login page', () => {
    cy.visit('/login');
    cy.url().should('include', '/login');
  });

  it('logs in a user', () => {
    cy.visit('/login');
    cy.get('[placeholder="username"]').type('user01');
    cy.get('[placeholder="password"]').type('secret');
    cy.intercept('POST', '**/auth/token').as('login');
    cy.get('.center > :nth-child(8)').click();
    cy.wait('@login');
    cy.get('.center > :nth-child(11)').click();
    cy.get('h1').should('contain', 'Welcome, user01');
  });

  it('logs out', () => {
    cy.get('.center > :nth-child(14)').click();
    cy.get('h1').should('contain', 'Logged out successfully!');
  });
});
