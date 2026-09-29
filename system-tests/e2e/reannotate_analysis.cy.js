(Cypress.config('isInteractive') ? describe : describe.skip)('reannotate_analysis.cy.js', () => {
  beforeEach(() => {
    // cy.resetDatabase();
    // cy.visit('/');
  });

  it('annotations CPAM0046', () => {
    cy.getCookie('rosalution_TOKEN').then((cookie) => {
      const token = cookie.value;
      cy.request({
        method: 'POST',
        url: 'https://local.rosalution.cgds/rosalution/api/annotation/CPAM0046',
        headers: {
          'accept': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      }).then((response) => {
        expect(response.status).to.eq(202);
      });
    });
  });
});
