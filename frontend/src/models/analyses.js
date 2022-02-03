export default {
  async all() {
    return [
      {
        analysis_id: '10f7aa04-6adf-4538-a700-ebe2f519473f',
        name: 'MuscDyst_SU_fam1',
        description: 'Muscular Dystrofy is a thing',
        case_type: 'Cohort',
        samples: [
          {name: 'LW000001', appstash_id: '10f7aa04-6adf-4538'},
          {name: 'LW000002', appstash_id: 'a700-ebe2f519473f'},
        ],
        granting_source: 'UAB Peds Alexander/Lopez',
        version: 'v0.1',
        latest_status: 'Annotation',
        last_modified_date: '2020-10-15',
        analysis_created_date: '2020-11-02',
      },
      {
        id: '10342gs4-6adf-4538-a700-ebef319473f',
        name: 'MuscDyst_SU_fam2',
        description: 'Muscular Dystrofy is a thing',
        case_type: 'Proband',
        samples: [
          {name: 'LW000004', appstash_id: '10342gs4-6adf'},
          {name: 'LW000005', appstash_id: '4538-a700-ebef319473f'},
        ],
        granting_source: 'UAB Peds Alexander/Lopez',
        version: 'v0.1',
        latest_status: 'Ready',
        last_modified_date: '2020-10-15',
        analysis_created_date: '2020-11-02',
      },
      {
        id: '1aeg4-6d32f-4348-a700-ebef334gfsf',
        name: 'CF_TLOAF1',
        description: 'CF causes a lot of issues',
        case_type: 'Proband',
        samples: [{name: 'LW000012', appstash_id: 'eg4-6d32f-4348'}],
        granting_source: 'UWVM Farrell',
        version: 'v0.1',
        latest_status: 'Active',
        last_modified_date: '2020-10-15',
        analysis_created_date: '2020-11-02',
      },
      {
        id: 'e99def4b-cdb3-4a6b-82f1-e3ab4df37f9f',
        name: 'CF_TLOAF2',
        description: 'CF causes a lot of issues',
        case_type: 'Cohort',
        samples: [{name: 'LW000013', appstash_id: 'eg4-6d32fdsasf-4348'}],
        granting_source: 'UWVM Farrell',
        version: 'v1.22.2',
        latest_status: 'Review',
        last_modified_date: '2020-10-15',
        analysis_created_date: '2020-11-02',
      },
      {
        id: 'e99def4b-cdb3-4a6b-82f2-e3ab4df37f9f',
        name: 'CF_TLOAF3',
        description: 'CF causes a lot of issues',
        case_type: 'Proband',
        samples: [{name: 'LW000014', appstash_id: 'egfdsd4-6d32fdsasf-4348'}],
        granting_source: 'UWVM Farrell',
        version: 'v0.1',
        latest_status: 'Group',
        last_modified_date: '2020-10-15',
        analysis_created_date: '2020-11-02',
      },
      {
        id: 'e99def4b-cdb3-4a6b-82f9-e3ab4df37f9f',
        name: 'CF_TLOAF4',
        description: 'CF causes a lot of issues',
        case_type: 'Proband',
        samples: [{name: 'LW000015', appstash_id: 'egfdsd4-asf-43548'}],
        granting_source: 'UWVM Farrell',
        version: 'v0.1',
        latest_status: 'Review',
        last_modified_date: '2020-10-15',
        analysis_created_date: '2020-11-02',
      },
      {
        id: '04910e36-1f3b-46cb-bc99-3c3bd232a4c6',
        name: 'CF_TLOAF_affected',
        description: 'CF causes a lot of issues',
        case_type: 'Proband',
        samples: [
          {name: 'LW000013', appstash_id: 'eg4-6d32fdsasf-4348'},
          {name: 'LW000014', appstash_id: 'egfdsd4-6d32fdsasf-4348'},
        ],
        granting_source: 'UWVM Farrell',
        version: 'v0.1',
        latest_status: 'Report',
        last_modified_date: '2020-10-15',
        analysis_created_date: '2020-11-02',
      },
      {
        id: 'd2218a06-47ec-482a-b316-927e219cef99',
        name: 'CF_Affected',
        description:
          'This CF case presents at different levels of severity potentially due to modifiers',
        case_type: 'Cohort',
        samples: [
          {name: 'LW000001', appstash_id: '10f7aa04-6adf-4538'},
          {name: 'LW000004', appstash_id: '10342gs4-6adf'},
        ],
        granting_source: 'UWVM Farrell',
        version: 'v0.1',
        latest_status: 'Group',
        last_modified_date: '2020-10-15',
        analysis_created_date: '2020-11-02',
      },
    ];
  },

  async getAnalysis(analysisId) {
    const analysisList = await this.all();
    return analysisList.find(({analysis_id: id}) => id === analysisId);
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
  },
};
