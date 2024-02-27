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
  let mockPostRequest;

  beforeEach(() => {
    mockGetRequest = sandbox.stub(Requests, 'get');
    mockPostFormResponse = sandbox.stub(Requests, 'postForm');
    mockPutFormResponse = sandbox.stub(Requests, 'putForm');
    mockDeleteRequest = sandbox.stub(Requests, 'delete');
    mockPutRequest = sandbox.stub(Requests, 'put');
    mockPostRequest = sandbox.stub(Requests, 'post');
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

  describe('sections', () => {
    describe('text within sections for analyses', () => {
      it('saves the changes for multiple rows of text within different sections', () => {
        const fixtureUpdates = {
          'Brief': {
            'Nominator': ['Dr. Person One With '],
            'ACMG Criteria To Add': ['Feeling To be Done'],
            'ACMG Classification Criteria': ['fdsfdsrewrewr'],
          },
          'Clinical History': {
            'Systems': ['Musculoskeletal and orthopedics fdsfds'],
            'Sequencing': ['WGS by the ????fdsfdsfds'],
          },
        };

        Analyses.updateAnalysisSections('CPAM0002', fixtureUpdates);

        expect(mockPostRequest.getCall(0).args[0]).to.equal(
            '/rosalution/api/analysis/CPAM0002/sections/batch',
        );
        expect(mockPostRequest.getCall(0).args[1]).to.have.lengthOf(2);
        expect(mockPostRequest.getCall(0).args[1][0].header).to.equal('Brief');
        expect(mockPostRequest.getCall(0).args[1][0].content).to.have.lengthOf(3);
      });
    });

    describe('images within sections for analyses', () => {
      it('attaches an image to a section', async () => {
        const mockImageId = '65b181c992f5d6edf214f9d1-new';
        mockPostFormResponse.resolves(getMockSectionsWithImageId(mockImageId));
        const fakeImageData = 'jklfdjlskfjal;fjdkl;a';
        const actualField = await Analyses.attachSectionImage('CPAM0002', 'Pedigree', 'Pedigree', fakeImageData);
        expect(mockPostFormResponse.called).to.be.true;
        expect(actualField.value[0]['file_id']).to.equal(mockImageId);
      });

      it('updates an image in a section', async () => {
        const mockImageId = '65b181c992f5d6edf214f9d1-updated';
        mockPutFormResponse.resolves(getMockSectionsWithImageId(mockImageId));
        const fakeImageData = 'updated-jklfdjlskfjal;fjdkl;a';
        await Analyses.updateSectionImage('CPAM0002', 'Pedigree', fakeImageData);
        expect(mockPutFormResponse.called).to.be.true;
      });
    });
  });

  describe('managing discussion posts for an analysis', () => {
    it('adds a new post to a discussion in an analysis', async () => {
      mockPostFormResponse.resolves({success: 'yay!'});

      const analysisName = 'CPAM0002';
      const postContent = 'Hello Frontend Unit Test!';

      await Analyses.postNewDiscussionThread(analysisName, postContent);

      expect(mockPostFormResponse.called).toBe(true);
    });

    it('deletes a discussion post in an analysis', async () => {
      const analysisName = 'CPAM0002';
      const postContent = 'Hello Frontend Unit Test!';

      await Analyses.deleteDiscussionThreadById(analysisName, postContent);

      expect(mockDeleteRequest.called).toBe(true);
    });
  });
});

/**
 * Returns valid sections that include an image within the Pedigree section
 * @param {string} fileImageId file_id string that is generated when saving a file
 * @return {Object} returns several analysis sections in a list that includes the pedigree section with an image
 */
function getMockSectionsWithImageId(fileImageId = 'default-image-id') {
  return [{
    'header': 'Pedigree',
    'attachment_field': 'Pedigree',
    'content': [
      {
        'type': 'images-dataset',
        'field': 'Pedigree',
        'value': [
          {
            'file_id': fileImageId,
          },
        ],
      },
    ],
  }, {
    'header': 'VMA21 Gene To Phenotype',
    'attachment_field': 'VMA21 Gene To Phenotype',
    'content': [
      {
        'type': 'images-dataset',
        'field': 'VMA21 Gene To Phenotype',
        'value': [],
      },
    ],
  }];
}

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
