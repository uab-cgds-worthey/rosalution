import Requests from '@/requests.js';
export default {
  async all() {
    const baseUrl = '/api/';
    const urlQuery = 'analysis';
    const body = await Requests.get(baseUrl + urlQuery);
    if ('errors' in body) {
      const errorString = body.data.errors.map((error) => error.message).join('; ');
      throw new Error('Failed to fetch analyses: ' + errorString);
    }
    return body;
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
