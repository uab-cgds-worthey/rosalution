import {describe, it, expect, beforeEach, afterEach} from 'vitest';

import Annotations from '@/models/annotations.js';
import Requests from '@/requests.js';
import sinon from 'sinon';

describe('analyses.js', () => {
  const sandbox = sinon.createSandbox();
  let mockGetRequest;

  beforeEach(() => {
    mockGetRequest = sandbox.stub(Requests, 'get');
  });

  afterEach(() => {
    sandbox.restore();
  });

  it('Querie a gene and variants annotations', async () => {
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
});
