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
  async attachAnnotationImage(annotation, image) {
    const baseUrl = '/rosalution/api/annotate';

    console.log(`${baseUrl}/${annotation.genomic_unit}/attach/image`);

    const attachmentForm = {
      'upload_file': image,
      'section_name': annotation.section,
    };

    return await Requests.postForm(`${baseUrl}/${annotation.genomic_unit}/attach/image`, attachmentForm);
  },
};
