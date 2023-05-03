import Requests from '@/requests.js';

export default {
  async getAnnotations(analysisName, gene, variant) {
    const baseUrl = '/rosalution/api/annotate';

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
      Requests.get(`${baseUrl}/gene/${gene}`),
      ...insertIf(variant !== '', Requests.get(`${baseUrl}/hgvsVariant/${variantWithoutProtein}`)),
    ]);
    return {...geneAnnotations, ...variantAnnotations};
  },
  async attachAnnotationImage(genomicUnit, dataSet, annotation) {
    const baseUrl = '/rosalution/api/annotate';

    const attachmentForm = {
      'genomic_unit_type': annotation.genomic_unit_type,
      'upload_file': annotation.annotation_data,
    };

    return await Requests.postForm(`${baseUrl}/${genomicUnit}/${dataSet}/attach/image`, attachmentForm);
  },
  async updateAnnotationImage(genomicUnit, dataSet, oldFileId, annotation) {
    const baseUrl = '/rosalution/api/annotate';

    const attachmentForm = {
      'genomic_unit_type': annotation.genomic_unit_type,
      'upload_file': annotation.annotation_data,
    };

    return await Requests.postForm(`${baseUrl}/${genomicUnit}/${dataSet}/update/${oldFileId}`, attachmentForm);
  },
  async removeAnnotationImage(genomicUnit, dataSet, fileId, annotation) {
    const baseUrl = '/rosalution/api/annotate';

    const attachmentForm = {
      'genomic_unit_type': annotation.genomic_unit_type,
    };

    const success = await Requests.deleteForm(
        `${baseUrl}/${genomicUnit}/${dataSet}/remove/${fileId}`, attachmentForm,
    );

    return success;
  },
};
