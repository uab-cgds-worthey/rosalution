import {describe, it, expect, beforeEach, afterEach} from 'vitest';

import Analyses from '@/models/analyses.js';
import Requests from '@/requests.js';
import sinon from 'sinon';

describe('analyses.js', () => {
  const sandbox = sinon.createSandbox();
  let mockGetRequest;
  let mockPostFormResponse;

  beforeEach(() => {
    mockGetRequest = sandbox.stub(Requests, 'get');
    mockPostFormResponse = sandbox.stub(Requests, 'postForm');
  });

  afterEach(() => {
    sandbox.restore();
  });

  it('Queries all the analyses', async () => {
    mockGetRequest.returns(allSummaries);
    const allAnalyses = await Analyses.all();
    expect(allAnalyses.length).to.equal(4);
  });

  it('Queries a specific analysis', async () => {
    mockGetRequest.returns(byName);
    const analysisName = 'CPAM0002';
    const specificAnalysis = await Analyses.getAnalysis(analysisName);

    expect(specificAnalysis.name).to.equal('CPAM0002');
    expect(specificAnalysis.nominated_by).to.equal('Dr. Person One');
  });

  it('Imports a browser file to the Analysis API succesfully', async () => {
    mockPostFormResponse.returns({sucess: 'yay'});
    await Analyses.importPhenotipsAnalysis(incomingCreateAnalysisFormFixture);
    expect(mockPostFormResponse.called).to.be.true;
  });

  it('attaches supporting evidence of a file', async () => {
    mockPostFormResponse.returns({sucess: 'yay'});
    await Analyses.attachSupportingEvidence('CPAM0002', {
      data: 'jfkldjafkdjafda',
      comment: 'Serious Things',
      type: 'file',
    });
    expect(mockPostFormResponse.called).to.be.true;
  });

  it('attaches supporting evidence of a file substitutes empty comments in', async () => {
    mockPostFormResponse.returns({sucess: 'yay'});
    await Analyses.attachSupportingEvidence('CPAM0002', {
      data: 'jfkldjafkdjafda',
      type: 'file',
    });
    expect(mockPostFormResponse.called).to.be.true;
  });

  it('attaches supporting evidence of a link', async () => {
    mockPostFormResponse.returns({sucess: 'yay'});
    await Analyses.attachSupportingEvidence('CPAM0002', {
      name: 'Best Website Ever',
      type: 'link',
      data: 'http://sites.uab.edu/cgds',
      comment: 'Serious Things',
    });
    expect(mockPostFormResponse.called).to.be.true;
  });

  it('attaches supporting evidence of a link substitutes empty comments in', async () => {
    mockPostFormResponse.returns({sucess: 'yay'});
    await Analyses.attachSupportingEvidence('CPAM0002', {
      name: 'Best Website Ever',
      type: 'link',
      data: 'http://sites.uab.edu/cgds',
    });
    expect(mockPostFormResponse.called).to.be.true;
  });


  it('attaches a section box image for analysis', async () => {
    mockPostFormResponse.returns({sucess: 'yay'});
    await Analyses.attachSectionBoxImage('CPAM0002', {
      'picture': 'this is three pictures in a trenchcoat',
    });
    expect(mockPostFormResponse.called).to.be.true;
  });
});

const allSummaries = [
  {
    'name': 'CPAM0002',
    'description': ': LMNA-related congenital muscular dystropy',
  },
  {
    'name': 'CPAM0046',
    'description': ': LMNA-related congenital muscular dystropy',
  },
  {
    'name': 'CPAM0047',
    'description': 'Congenital variant of Rett syndrome',
  },
  {
    'name': 'CPAM0053',
    'description': 'Mild Zellweger Spectrum Disorder, a Peroxisome Biogenesis Disorder',
  },
];

const byName = {
  'name': 'CPAM0002',
  'description': ': LMNA-related congenital muscular dystropy',
  'nominated_by': 'Dr. Person One',
};

const incomingCreateAnalysisFormFixture = {
  name: 'Fake Analysis',
  description: 'Fake Description',
  samples: [
    {
      name: 'Fake Sample',
      sources: [
        {
          secondaryAnalysis: [
            {
              annotations: {
                coordinateList: [
                  {
                    chromosome: '17',
                    position: '3768176',
                    reference: 'T',
                    alternate: 'AGTGT',
                  },
                  {
                    chromosome: '36',
                    position: '2781',
                    reference: 'GTATAGCA',
                    alternate: 'GTCTATTTT',
                  },
                  {
                    chromosome: '1',
                    position: '37',
                    reference: 'GATTTA',
                    alternate: 'AATTTAGA',
                  },
                  {
                    chromosome: '1',
                    position: '2',
                    reference: 'GAAAAT',
                    alternate: 'GGGTTTAAA',
                  },
                ],
                secondaryPipeline: 'sv',
              },
            },
          ],
        },
      ],
    },
  ],
};
