import Requests from '@/requests.js';


function encodeVariantSpecialCharacters(incomingVariant) {
  return incomingVariant.replaceAll('?', '%3F');
}

export default {
  async getAnnotations(analysisName, gene, variant) {
    const baseUrl = '/rosalution/api/analysis';

    const encodedVariantForUrl = encodeVariantSpecialCharacters(variant);

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
      ...insertIf(variant !== '', Requests.get(`${baseUrl}/${analysisName}/hgvsVariant/${encodedVariantForUrl}`)),
    ]);
    return {...geneAnnotations, ...variantAnnotations};
  },
  async attachAnnotationImage(genomicUnit, dataSet, annotation) {
    const baseUrl = `/rosalution/api/annotation`;

    const encodedGenomicUnit =
      (annotation.genomic_unit_type === 'hgvs_variant') ? encodeVariantSpecialCharacters(genomicUnit) : genomicUnit;


    const attachmentForm = {
      'upload_file': annotation.annotation_data,
    };

    const url = `${baseUrl}/${encodedGenomicUnit}/${dataSet}` +
      `/attachment?genomic_unit_type=${annotation.genomic_unit_type}`;

    return await Requests.postForm(url, attachmentForm);
  },
  async updateAnnotationImage(genomicUnit, dataSet, oldId, annotation) {
    const baseUrl = '/rosalution/api/annotation';

    const encodedGenomicUnit =
      (annotation.genomic_unit_type === 'hgvs_variant') ? encodeVariantSpecialCharacters(genomicUnit) : genomicUnit;

    const attachmentForm = {
      'upload_file': annotation.annotation_data,
    };

    const url = `${baseUrl}/${encodedGenomicUnit}/${dataSet}/`+
      `attachment/${oldId}?genomic_unit_type=${annotation.genomic_unit_type}`;

    return await Requests.putForm(url, attachmentForm);
  },
  async removeAnnotationImage(genomicUnit, dataSet, fileId, annotation) {
    const baseUrl = '/rosalution/api/annotation';

    const success = await Requests.delete(
        `${baseUrl}/${genomicUnit}/${dataSet}/attachment/${fileId}?genomic_unit_type=${annotation.genomic_unit_type}`);

    return success;
  },
};
