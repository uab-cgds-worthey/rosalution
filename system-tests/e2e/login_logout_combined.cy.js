describe('login_logout_combined.cy.js', () => {
  it('app url redirects to login page', () => {
    cy.visit('/login');
    cy.url().should('include', '/login');
  });

  it('logs in a user', () => {
    cy.visit('/login');
    cy.get('[data-test="username-input"]').type('user01');
    cy.get('[data-test="local-login-button"]').click();
    cy.get('[data-test="user-text"]').should('contain', 'user01');
  });

  it('logs out', () => {
    cy.get('.grey-rounded-menu').invoke('attr', 'style', 'display: block; visibility: visible; opacity: 1;');
    cy.get('.grey-rounded-menu > li').contains('Logout').click();
    cy.get('span').should('contain', 'Local Development Login');
  });
});
