import Requests from '@/requests.js';


function encodeVariantSpecialCharacters(incomingVariant) {
  return incomingVariant.replaceAll('?', '%3F');
}

export default {
  async getAnnotations(analysisName, gene, variant) {
    const baseUrl = '/rosalution/api/analysis';

    const annotationEndpoints = [`${baseUrl}/${analysisName}/gene/${gene}`];
    if ( variant && variant !== '' ) {
      const encodedVariantForUrl = encodeVariantSpecialCharacters(variant);
      annotationEndpoints.push(`${baseUrl}/${analysisName}/hgvsVariant/${encodedVariantForUrl}`);
    }

    const [geneAnnotations, variantAnnotations] = await Promise.all(
        annotationEndpoints.map( (endpoints) => Requests.get(endpoints) ),
    );
    return {...geneAnnotations, ...(variantAnnotations ? variantAnnotations : [])};
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
