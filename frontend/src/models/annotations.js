import Requests from '@/requests.js';

export default {
  async getAnnotations(analysisName, gene, variant) {
    const baseUrl = '/rosalution/api/analysis';

    const variantWithoutProtein = variant.replace(/\(.*/, '');

    /**
     * Inline helper method to determine if the variant annotations need to get queried.
     * This allows for ease of debugging and readability
     * @param {boolean} condition
     * @param  {Object} elements
     * @return {Array} If condition is true, returns the elements spread to be
     *                 populated in an array or an empty array
     */
    function insertIf(condition, ...elements) {
      return condition ? elements : [];
    }

    const [geneAnnotations, variantAnnotations] = await Promise.all([
      Requests.get(`${baseUrl}/${analysisName}/gene/${gene}`),
      ...insertIf(variant !== '', Requests.get(`${baseUrl}/${analysisName}/hgvsVariant/${variantWithoutProtein}`)),
    ]);
    return {...geneAnnotations, ...variantAnnotations};
  },
  async attachAnnotationImage(genomicUnit, dataSet, annotation) {
    const baseUrl = `/rosalution/api/annotation`;

    const attachmentForm = {
      'upload_file': annotation.annotation_data,
    };

    return await Requests.postForm(
        `${baseUrl}/${genomicUnit}/${dataSet}/attachment?genomic_unit_type=${annotation.genomic_unit_type}`,
        attachmentForm,
    );
  },
  async updateAnnotationImage(genomicUnit, dataSet, oldId, annotation) {
    const baseUrl = '/rosalution/api/annotation';

    const attachmentForm = {
      'upload_file': annotation.annotation_data,
    };

    return await Requests.putForm(
        `${baseUrl}/${genomicUnit}/${dataSet}/attachment/${oldId}?genomic_unit_type=${annotation.genomic_unit_type}`,
        attachmentForm,
    );
  },
  async removeAnnotationImage(genomicUnit, dataSet, fileId, annotation) {
    const baseUrl = '/rosalution/api/annotation';

    const success = await Requests.delete(
        `${baseUrl}/${genomicUnit}/${dataSet}/attachment/${fileId}?genomic_unit_type=${annotation.genomic_unit_type}`);

    return success;
  },
};
