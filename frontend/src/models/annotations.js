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
  async getAnnotationImage(fileId) {
    const url = `/rosalution/api/analysis/download/${fileId}`;
    return await Requests.getImage(url);
  },
  async attachAnnotationImage(annotation, image) {
    const baseUrl = '/rosalution/api/annotate';

    const attachmentForm = {
      'upload_file': image,
      'genomic_unit_type': annotation.genomic_unit_type,
      'section_name': annotation.section,
    };

    return await Requests.postForm(`${baseUrl}/${annotation.genomic_unit}/attach/image`, attachmentForm);
  },
};
