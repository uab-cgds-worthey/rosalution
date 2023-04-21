import {describe, it, expect, beforeEach, afterEach} from 'vitest';

import Annotations from '@/models/annotations.js';
import Requests from '@/requests.js';
import sinon from 'sinon';

describe('annotations.js', () => {
  const sandbox = sinon.createSandbox();
  let mockGetRequest;
  let mockPostFormRequest;
  let mockDeleteFormRequest;

  beforeEach(() => {
    mockGetRequest = sandbox.stub(Requests, 'get');
    mockPostFormRequest = sandbox.stub(Requests, 'postForm');
    mockDeleteFormRequest = sandbox.stub(Requests, 'deleteForm');
  });

  afterEach(() => {
    sandbox.restore();
  });

  it('Queries a gene and variants annotations', async () => {
    mockGetRequest.callsFake((url) => {
      if (url.includes('gene')) {
        return {
          'Gene Summary': 'This gene encodes a chaperone for assembly of lysosomal vacuolar ATPase.[provided by RefSeq',
          'ClinGen_gene_url': 'https://search.clinicalgenome.org/kb/genes/HGNC:22082',
        };
      }

      return {
        'CADD': 33,
        'ClinVar_variant_url': 'https://www.ncbi.nlm.nih.gov/clinvar/variation/581244',
      };
    });

    const annotations = await Annotations.getAnnotations('CPAM0002', 'VMA21', 'NM_001017980.3:c.164G>T');
    expect(annotations['Gene Summary']).to.include('chaperone');
    expect(annotations['ClinGen_gene_url']).to.equal('https://search.clinicalgenome.org/kb/genes/HGNC:22082');
    expect(annotations['CADD']).to.equal(33);
    expect(annotations['ClinVar_variant_url']).to.equal('https://www.ncbi.nlm.nih.gov/clinvar/variation/581244');
  });

  it('saves an image with its corresponding section name as expected', async () => {
    const expectedUrl = '/rosalution/api/annotate/SBFP1/Gene Homology/attach/image';
    const expectedFormData = {
      'genomic_unit_type': 'gene',
      'upload_file': 'fake-image-path-1',
    };
    const expectedReturn = 'it worked';

    mockPostFormRequest.returns(expectedReturn);

    const actualReturned = await Annotations.attachAnnotationImage(
        'SBFP1',
        'Gene Homology',
        {genomic_unit_type: 'gene', annotation_data: 'fake-image-path-1'},
    );

    expect(actualReturned).to.equal(expectedReturn);
    expect(mockPostFormRequest.calledWith(expectedUrl, expectedFormData)).to.be.true;
  });

  it('saves a new image over an existing image with its corresponding section name', async () => {
    const expectedUrl = '/rosalution/api/annotate/SBFP1/Gene Homology/update/old-fake-image-id-1';
    const expectedFormData = {'genomic_unit_type': 'gene', 'upload_file': 'fake-image-path-1'};

    const expectedReturn = 'it worked';

    mockPostFormRequest.returns(expectedReturn);

    const actualReturned = await Annotations.updateAnnotationImage(
        'SBFP1',
        'Gene Homology',
        'old-fake-image-id-1',
        {genomic_unit_type: 'gene', annotation_data: 'fake-image-path-1'},
    );

    expect(actualReturned).to.equal(expectedReturn);
    expect(mockPostFormRequest.calledWith(expectedUrl, expectedFormData)).to.be.true;
  });

  it('removes an image annotation from its corresponding section name', async () => {
    const expectedUrl = '/rosalution/api/annotate/SBFP1/Gene Homology/remove/fake-image-id-1';
    const expectedFormData = {
      'genomic_unit_type': 'gene',
    };

    const expectedReturn = 'it worked';

    mockDeleteFormRequest.returns(expectedReturn);

    const actualReturned = await Annotations.removeAnnotationImage(
        'SBFP1',
        'Gene Homology',
        'fake-image-id-1',
        {genomic_unit_type: 'gene'},
    );

    expect(actualReturned).to.equal(expectedReturn);
    expect(mockDeleteFormRequest.calledWith(expectedUrl, expectedFormData)).to.be.true;
  });
});
