import {describe, it, expect, beforeEach, afterEach} from 'vitest';

import Analyses from '@/models/analyses.js';
import Requests from '@/requests.js';
import sinon from 'sinon';

describe('analyses.js', () => {
  const sandbox = sinon.createSandbox();
  let mockGetRequest;
  let mockPostFormResponse;
  let mockPutFormResponse;
  let mockDeleteRequest;
  let mockPutRequest;

  beforeEach(() => {
    mockGetRequest = sandbox.stub(Requests, 'get');
    mockPostFormResponse = sandbox.stub(Requests, 'postForm');
    mockPutFormResponse = sandbox.stub(Requests, 'putForm');
    mockDeleteRequest = sandbox.stub(Requests, 'delete');
    mockPutRequest = sandbox.stub(Requests, 'put');
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

  it('Queries a specific summary by name', async () => {
    mockGetRequest.returns(byName);
    const analysisName = 'CPAM0002';
    const specificSummary = await Analyses.getSummaryByName(analysisName);

    expect(specificSummary.name).to.equal('CPAM0002');
    expect(specificSummary.nominated_by).to.equal('Dr. Person One');
    expect(specificSummary.monday_com).to.equal('https://monday.com');
  });

  it('Imports a browser file to the Analysis API succesfully', async () => {
    mockPostFormResponse.returns({sucess: 'yay'});
    await Analyses.importPhenotipsAnalysis(incomingCreateAnalysisFormFixture);
    expect(mockPostFormResponse.called).to.be.true;
  });

  it('Marks an analysis ready', async () => {
    await Analyses.pushAnalysisEvent('CPAM0002', Analyses.EventType.READY);
    expect(mockPutRequest.called).to.be.true;
  });

  describe('supporting evidence', () => {
    it('attaches as a file', async () => {
      mockPostFormResponse.returns({sucess: 'yay'});
      await Analyses.attachSupportingEvidence('CPAM0002', {
        data: 'jfkldjafkdjafda',
        comment: 'Serious Things',
        type: 'file',
      });
      expect(mockPostFormResponse.called).to.be.true;
    });

    it('attaches as a file with empty comments', async () => {
      mockPostFormResponse.returns({sucess: 'yay'});
      await Analyses.attachSupportingEvidence('CPAM0002', {
        data: 'jfkldjafkdjafda',
        type: 'file',
      });
      expect(mockPostFormResponse.called).to.be.true;
    });

    it('attaches as a link', async () => {
      mockPostFormResponse.returns({sucess: 'yay'});
      await Analyses.attachSupportingEvidence('CPAM0002', {
        name: 'Best Website Ever',
        type: 'link',
        data: 'http://sites.uab.edu/cgds',
        comment: 'Serious Things',
      });
      expect(mockPostFormResponse.called).to.be.true;
    });

    it('attaches as link substitutes with empty comments', async () => {
      mockPostFormResponse.returns({sucess: 'yay'});
      await Analyses.attachSupportingEvidence('CPAM0002', {
        name: 'Best Website Ever',
        type: 'link',
        data: 'http://sites.uab.edu/cgds',
      });
      expect(mockPostFormResponse.called).to.be.true;
    });

    it('removes supporting evidence', async () => {
      await Analyses.removeSupportingEvidence('CPAM0002', 'remove-attach-it-now');
      expect(mockDeleteRequest.called).to.be.true;
    });
  });

  describe('section images for analysis', () => {
    it('attaches an image to a section', async () => {
      mockPostFormResponse.returns({sucess: 'yay'});
      const fakeImageData = 'jklfdjlskfjal;fjdkl;a';
      await Analyses.attachSectionImage('CPAM0002', 'Pedigree', fakeImageData);
      expect(mockPostFormResponse.called).to.be.true;
    });

    it('updates an image in a section', async () => {
      mockPutFormResponse.resolves({sucess: 'yay'});
      const fakeImageData = 'updated-jklfdjlskfjal;fjdkl;a';
      await Analyses.updateSectionImage('CPAM0002', 'Pedigree', fakeImageData);
      expect(mockPutFormResponse.called).to.be.true;
    });
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
  'monday_com': 'https://monday.com',
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
