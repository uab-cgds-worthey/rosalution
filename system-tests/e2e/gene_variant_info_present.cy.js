describe('gene_variant_info_present.cy.js', () => {
  beforeEach(() => {
    cy.visit('/');
    cy.get('[href="/rosalution/analysis/CPAM0047"]').click();
  });

  it('has link to gnomAD for the gene variant annotation and it would open in new tab', () => {
    cy.get('[data-test="gene-name"]').click();
    cy.get('[data-test="gnomAD_gene_url"]').should('have.attr', 'href', 'https://gnomad.'+
    'broadinstitute.org/gene/ENSG00000100241?dataset=gnomad_r2_1');
    cy.get('[data-test="gnomAD_gene_url"]').should('have.attr', 'target', '_blank');
    cy.get('[data-test="gnomAD_gene_url"]').should('have.attr', 'class', 'linkout linkout-available');
    cy.get('[data-test="gnomAD_gene_url"]').should('have.attr', 'rel', 'noreferrer noopener');
    cy.get('[data-test="gnomAD_gene_url"]').then((link) => {
      cy.request(link.prop('href')).its('status').should('eq', 200);
    });
  });

  it('has link to ClinGen for the gene variant annotation and it would open in new tab', () => {
    cy.get('[data-test="gene-name"]').click();
    cy.get('[data-test="ClinGen_gene_url"]').should('have.attr', 'href', 'https://search.'+
    'clinicalgenome.org/kb/genes/HGNC:10542');
    cy.get('[data-test="ClinGen_gene_url"]').should('have.attr', 'target', '_blank');
    cy.get('[data-test="ClinGen_gene_url"]').should('have.attr', 'class', 'linkout linkout-available');
    cy.get('[data-test="ClinGen_gene_url"]').should('have.attr', 'rel', 'noreferrer noopener');
    cy.get('[data-test="ClinGen_gene_url"]').then((link) => {
      cy.request(link.prop('href')).its('status').should('eq', 200);
    });
  });

  it('has link to NCBI for the gene variant annotation and it would open in new tab', () => {
    cy.get('[data-test="gene-name"]').click();
    cy.get('[data-test="NCBI_gene_url"]').should('have.attr', 'href', 'https://www.ncbi.'+
    'nlm.nih.gov/gene?Db=gene&Cmd=DetailsSearch&Term=6305');
    cy.get('[data-test="NCBI_gene_url"]').should('have.attr', 'target', '_blank');
    cy.get('[data-test="NCBI_gene_url"]').should('have.attr', 'class', 'linkout linkout-available');
    cy.get('[data-test="NCBI_gene_url"]').should('have.attr', 'rel', 'noreferrer noopener');
    cy.get('[data-test="NCBI_gene_url"]').then((link) => {
      cy.request(link.prop('href')).its('status').should('eq', 200);
    });
  });
});
