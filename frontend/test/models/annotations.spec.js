import {describe, it, expect, beforeEach, afterEach} from 'vitest';

import Annotations from '@/models/annotations.js';
import Requests from '@/requests.js';
import sinon from 'sinon';

describe('analyses.js', () => {
  const sandbox = sinon.createSandbox();
  let mockGetRequest;
  let mockPostFormRequest;

  beforeEach(() => {
    mockGetRequest = sandbox.stub(Requests, 'get');
    mockPostFormRequest = sandbox.stub(Requests, 'postForm');
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
    const expectedUrl = '/rosalution/api/annotate/SBFP1/attach/image';
    const expectedFormData = {
      'upload_file': 'file here',
      'section_name': 'Gene Homology',
      'genomic_unit_type': 'gene',
    };
    const expectedReturn = 'it worked';

    mockPostFormRequest.returns(expectedReturn);

    const actualReturned = await Annotations.attachAnnotationImage({
      genomic_unit: 'SBFP1',
      section: 'Gene Homology',
      genomic_unit_type: 'gene',
    }, 'file here');

    expect(actualReturned).to.equal(expectedReturn);
    expect(mockPostFormRequest.calledWith(expectedUrl, expectedFormData)).to.be.true;
  });
});
