import {describe, it, expect} from 'vitest';

import Analyses from '@/models/analyses.js';

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

describe('analyses.js', () => {
  it('Queries all the analyses', async () => {
    const allAnalyses = await Analyses.all();
    expect(allAnalyses.length).toBe(8);
  });

  it('Queries a specific analysis', async () => {
    const analysisId = 'e99def4b-cdb3-4a6b-82f1-e3ab4df37f9f';
    const specificAnalysis = await Analyses.getAnalysis(analysisId);

    expect(specificAnalysis.name).toBe('CF_TLOAF2');
  });

  it.only('Formats the formData to be sent off and saved', async () => {
    const fakeFormInput = await Analyses.saveAnalysis(incomingCreateAnalysisFormFixture);

    expect(fakeFormInput).to.not.be.undefined;
  });
});
