export default {
  async all() {
    return [
      {
        analysis_id: '10f7aa04-6adf-4538-a700-ebe2f519473f',
        name: 'CPAM0046',
        description: ': LMNA-related congenital muscular dystropy',
        genomic_units: [
          {gene: 'LMNA'},
          {transcript: 'NM_170707.3'},
          {chromosome: '1', position: 156134885, reference: 'C', alternate: 'T'},
        ],
        nominator: 'Dr. Person Two',
        latest_status: 'Approved',
        created_date: '2021-09-30',
        last_modified_date: '2021-10-01',
      },
      {
        id: 'e99def4b-cdb3-4a6b-82f1-e3ab4df37f9f',
        name: 'CPAM0047',
        description: 'Congenital variant of Rett syndrome',
        genomic_units: [
          {gene: 'SBF1'},
          {transcript: 'NM_002972.2'},
          {chromosome: '1', pos: '5474', ref: 'T', alt: 'G'},
        ],
        nominator: 'CMT4B3 Foundation',
        latest_status: 'Declined',
        created_date: '2020-12-03',
        last_modified_date: '2021-12-12',
      },
      {
        id: '10342gs4-6adf-4538-a700-ebef319473f',
        name: 'CPAM0053',
        description:
          'Mild Zellweger Spectrum Disorder, a Peroxisome Biogenesis Disorder',
        genomic_units: [
          {gene: 'PEX10'},
          {transcript: 'NM_153818.2'},
          {chromosome: '1', position: 2406528, reference: 'C', alternate: 'G'},
        ],
        nominator: 'N/A',
        latest_status: 'Ready',
        created_date: '2021-11-02',
        last_modified_date: '2021-11-23',
      },
      {
        id: '1aeg4-6d32f-4348-a700-ebef334gfsf',
        name: 'CPAM0065',
        description: 'Congenital variant of Rett syndrome',
        genomic_units: [
          {gene: 'FOXG1'},
          {transcript: 'NM_005249.5'},
          {chromosome: '1', pos: '924', ref: 'G', alt: 'A'},
        ],
        nominator: 'Believe in a Cure Foundation',
        latest_status: 'Declined',
        created_date: '2020-12-03',
        last_modified_date: '2021-12-12',
      },
    ];
  },

  async getAnalysis(analysisId) {
    const analysisList = await this.all();
    return analysisList.find(({id}) => id === analysisId);
  },

  async saveAnalysis(formData) {
    // Linting - Assigned but never used
    // const url = '/sample/analysis';

    const formInput = {
      analysisJson: {
        name: formData.name,
        description: formData.description,
        samples: [],
        annotations: {
          case_type: 'proband',
          granting_source: 'UW Madison',
          comments: 'IT will be what it must be',
        },
      },
    };

    formData.samples.forEach((sample, index) => {
      formInput.analysisJson.samples.push(sample.name);

      const sampleFormFieldName = `sample${index + 1}Json`;
      formInput[sampleFormFieldName] = JSON.stringify({
        name: sample.name,
        sources: sample.sources,
      });

      formInput.analysisJson = JSON.stringify(formInput.analysisJson);
    });

    // Here is where we posting a request with our formatted formInput and URL
    // await Requests.postForm(url, formInput);

    // Returning for now to ensure data is correct
    return formInput;
  },
};
