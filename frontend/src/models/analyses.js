import Requests from '@/requests.js';
export default {
  async all() {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'analysis/summary';
    return await Requests.get(baseUrl + urlQuery);
  },

  async getAnalysis(analysisName) {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'analysis/' + analysisName;
    return await Requests.get(baseUrl + urlQuery);
  },

  async importPhenotipsAnalysis(file) {
    const url = '/rosalution/api/analysis/import_file';

    const fileUploadFormData = {
      'phenotips_file': file,
    };

    return Requests.postForm(url, fileUploadFormData);
  },
};
