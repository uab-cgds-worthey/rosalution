import Requests from '@/requests.js';

export default {
  async getAnnotations(analysisName, gene, variant) {
    const baseUrl = '/rosalution/api/annotate';

    const [geneAnnotations, variantAnnotations] = await Promise.all([
      Requests.get(`${baseUrl}/gene/${gene}`),
      Requests.get(`${baseUrl}/hgvsVariant/${variant}`),
    ]);
    return {...geneAnnotations, ...variantAnnotations};
  },
};
