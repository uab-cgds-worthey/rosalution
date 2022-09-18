import Requests from '@/requests.js';
export default {
  async all() {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'analysis/summary';
    const body = await Requests.get(baseUrl + urlQuery);
    if ('errors' in body) {
      const errorString = body.data.errors.map((error) => error.message).join('; ');
      throw new Error('Failed to fetch analyses: ' + errorString);
    }
    return body;
  },

  async getAnalysis(analysisName) {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'analysis/' + analysisName;
    const body = await Requests.get(baseUrl + urlQuery);
    if ('errors' in body) {
      const errorString = body.data.errors.map((error) => error.message).join('; ');
      throw new Error('Failed to fetch analyses: ' + errorString);
    }
    return body;
  },

  async importPhenotipsAnalysis(file) {
    console.log("saving a new analysis")
    const url = '/rosalution/api/analysis/import';
    const body = await Requests.post(url, file);
    if ('errors' in body) {
      const errorString = body.data.errors.map((error) => error.message).join('; ');
      throw new Error('Failed to fetch analyses: ' + errorString);
    }
    return body;
  },
};
