import Requests from '@/requests.js';
export default {
  async all() {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'analysis/summary';
    const analysesSummary = await Requests.get(baseUrl + urlQuery);
    return analysesSummary;
  },

  async getSummaryByName(analysisName) {
    const url = `/rosalution/api/analysis/summary/${analysisName}`;
    const analysisSummary = await Requests.get(url);
    return analysisSummary;
  },

  async getAnalysis(analysisName) {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'analysis/' + analysisName;
    const body = await Requests.get(baseUrl + urlQuery);
    return body;
  },

  async getGenomicUnits(analysisName) {
    const url = `/rosalution/api/analysis/${analysisName}/genomic_units`;
    const genomicUnits = await Requests.get(url);
    return genomicUnits;
  },

  async updateAnalysisSections(analysisName, updatedSections) {
    const url = `/rosalution/api/analysis/${analysisName}/update/sections`;
    return await Requests.put(url, updatedSections);
  },

  async markAnalysisReady(analysisName) {
    const url = `/rosalution/api/analysis/${analysisName}/mark_ready`;
    return await Requests.put(url);
  },

  async markAnalysisActive(analysisName) {
    // const url = `/rosalution/api/analysis/${analysisName}/mark_active`;
    // return await Requests.put(url);
    console.warn('Mark analysis active does not exist yet');
    //  ** Not implemented yet **
  },

  async getAnnotationConfiguration(analysisName) {
    // const baseUrl = '/rosalution/api/';
    // const urlQuery = `analysis/{analysisName}`;

    return annotationRenderingTemporary;
  },

  async importPhenotipsAnalysis(file) {
    const url = '/rosalution/api/analysis/import_file';

    const fileUploadFormData = {
      'phenotips_file': file,
    };

    return Requests.postForm(url, fileUploadFormData);
  },

  async getSectionImage(fileId) {
    const url = `/rosalution/api/analysis/download/${fileId}`;
    return await Requests.getImage(url);
  },

  async attachSectionImage(analysisName, sectionName, image) {
    if ('Pedigree' != sectionName) {
      throw Error(`Only support for removing Pedigree. Failed to remove image for section '${sectionName}'.`);
    }

    const url = `/rosalution/api/analysis/${analysisName}/attach/pedigree`;

    const attachmentForm = {
      'upload_file': image,
    };

    return await Requests.postForm(url, attachmentForm);
  },

  async updateSectionImage(analysisName, sectionName, image) {
    if ('Pedigree' != sectionName) {
      throw Error(`Only support for removing Pedigree. Failed to remove image for section '${sectionName}'.`);
    }

    const url = `/rosalution/api/analysis/${analysisName}/update/pedigree`;

    const updateForm = {
      'upload_file': image,
    };

    return await Requests.putForm(url, updateForm);
  },

  async removeSectionImage(analysisName, sectionName) {
    if ('Pedigree' != sectionName) {
      throw Error(`Only support for removing Pedigree. Failed to remove image for section '${sectionName}'.`);
    }

    const url = `/rosalution/api/analysis/${analysisName}/remove/pedigree`;
    const success = await Requests.delete(url);
    return success;
  },

  async attachSupportingEvidence(analysisName, evidence) {
    let attachmentForm = null;
    let url = `/rosalution/api/analysis/${analysisName}/attach`;

    if (evidence.type == 'file') {
      attachmentForm = {
        'upload_file': evidence.data,
        'comments': evidence.comments ? evidence.comments : '  ', /** Required for now, inserting empty string */
      };
      url += '/file';
    } else if ( evidence.type == 'link') {
      attachmentForm = {
        'link_name': evidence.name,
        'link': evidence.data,
        'comments': evidence.comments ? evidence.comments : '  ', /** Required for now, inserting empty string */
      };
      url += '/link';
    }

    if (null == attachmentForm) {
      throw new Error(`Evidence attachment ${evidence} type is invalid.`);
    }

    return await Requests.postForm(url, attachmentForm);
  },

  async updateSupportingEvidence(analysisName, evidence) {
    const url = `/rosalution/api/analysis/${analysisName}/attachment/${evidence.attachment_id}/update`;

    const attachmentForm = {
      name: evidence.name,
      ...('link' == evidence.type) && {data: evidence.data},
      comments: evidence.comments,
    };

    return await Requests.putForm(url, attachmentForm);
  },

  async removeSupportingEvidence(analysisName, attachmentId) {
    const url = `/rosalution/api/analysis/${analysisName}/attachment/${attachmentId}/remove`;
    const success = await Requests.delete(url);
    return success;
  },

  async downloadSupportingEvidence(attachmentId, attachmentFile) {
    const url = `/rosalution/api/analysis/download/${attachmentId}`;
    const fileData = {'filename': attachmentFile};
    return Requests.getDownload(url, fileData);
  },

  async attachThirdPartyLink(analysisName, linkType, link) {
    const url = `/rosalution/api/analysis/${analysisName}/attach/${linkType}`;
    const attachmentForm = {
      'link': link,
    };
    return await Requests.putForm(url, attachmentForm);
  },
};

const annotationRenderingTemporary = [
  {
    'type': 'section',
    'class': '',
    'header': 'gene',
    'anchor': 'Gene',
    'header_datasets': [{
      'dataset': 'ClinGen_gene_url',
      'type': 'icon-linkout-dataset',
      'props': {
        'imageFilename': 'logo-clin-gen.svg',
        'altText': 'Clinical Genomic Resource Gene Linkout',
      },
    }, {
      'dataset': 'NCBI_gene_url',
      'type': 'icon-linkout-dataset',
      'props': {
        'imageFilename': 'ncbi-logo.png',
        'altText': 'National Center for Biotechnology Information Gene Linkout',
      },
    }, {
      'dataset': 'gnomAD_gene_url',
      'type': 'icon-linkout-dataset',
      'props': {
        'imageFilename': 'gnomad-logo.png',
        'altText': 'Genome Aggregation Database (gnomAD) from Broad Institute',
      },
    }],
    'rows': [
      {
        'class': '',
        'datasets': [
          {
            'dataset': 'Gene Summary',
            'type': 'text-dataset',
            'props': {
            },
          },
        ],
      },
      {
        'class': '',
        'datasets': [
          {
            'dataset': 'OMIM',
            'type': 'text-dataset',
            'linkout_dataset': 'OMIM_gene_search_url',
            'props': {
              'label': 'OMIM',
            },
          },
        ],
      }, {
        'class': '',
        'datasets': [
          {
            'dataset': 'HPO',
            'type': 'text-dataset',
            'linkout_dataset': 'HPO_gene_search_url',
            'props': {
              'label': 'HPO',
            },
          },
        ],
      },
    ],
  },
  {
    'type': 'section',
    'class': '',
    'header': 'variant',
    'anchor': 'Variant',
    'header_datasets': [],
    'rows': [
      {
        'class': '',
        'datasets': [
          {
            'dataset': 'CADD',
            'type': 'score-dataset',
            'props': {
              'label': 'CADD',
              'minimum': -10,
              'maximum': 99,
              'bounds': {
                'lowerBounds': 0.9,
                'upperBounds': 1.33,
              },
              'cutoff': 15,
            },
          },
          // {
          //   'dataset': 'Phylop100',
          //   'type': 'score-dataset',
          //   'props': {
          //     'label': 'Phylop100',
          //   },
          // },
        ],
      },
      {
        'class': '',
        'datasets': [
          // {
          //   'dataset': 'GERP',
          //   'type': 'score-dataset',
          //   'props': {
          //     'label': 'GERP',
          //     'minimum': -13.1,
          //     'maximum': 6.54,
          //   },
          // },
          // {
          //   'dataset': 'Mappability',
          //   'type': 'score-dataset',
          //   'props': {
          //     'label': 'Mappability',
          //     'minimum': -13.1,
          //     'maximum': 6.54,
          //   },
          // },
        ],
      },
      {
        'datasets': [
          {
            'dataset': 'ClinVar',
            'type': 'clinvar-dataset',
            'linkout_dataset': 'ClinVar_variant_url',
            'props': {
              'label': 'ClinVar',
            },
          },
        ],
      },
      {
        'datasets': [
          {
            'dataset': 'transcripts',
            'genomicType': 'hgvs_variant',
            'type': 'transcript-datasets',
          },
        ],
      },
    ],
  },
  {
    'type': 'section',
    'class': '',
    'header': 'Chromosomal Localization',
    'anchor': 'Chromosomal_Localization',
    'header_datasets': [],
    'props': {
      'attachmentDataset': 'Chromosomal_Localization',
      'genomicAttachmentType': 'hgvs_variant',
    },
    'rows': [{
      'class': '',
      'datasets': [
        {
          'dataset': 'Chromosomal_Localization',
          'genomicType': 'hgvs_variant',
          'type': 'images-dataset',
        },
      ],
    }],
  },
  {
    'type': 'section',
    'class': '',
    'header': 'Secondary Structure',
    'anchor': 'Secondary_Structure',
    'header_datasets': [],
    'props': {
      'attachmentDataset': 'Secondary_Structure',
      'genomicAttachmentType': 'hgvs_variant',
    },
    'rows': [{
      'class': '',
      'datasets': [
        {
          'dataset': 'Secondary_Structure',
          'genomicType': 'hgvs_variant',
          'type': 'images-dataset',
        },
      ],
    }],
  },
  {
    'type': 'section',
    'class': '',
    'header': 'Causal Variant In This Locus (ClinVar)',
    'anchor': 'Causal_Variant',
    'header_datasets': [],
    'props': {
      'attachmentDataset': 'Causal_Variant_In_This_Locus_ClinVar',
      'genomicAttachmentType': 'hgvs_variant',
    },
    'rows': [{
      'class': '',
      'datasets': [
        {
          'dataset': 'Causal_Variant_In_This_Locus_ClinVar',
          'genomicType': 'hgvs_variant',
          'type': 'images-dataset',
        },
      ],
    }],
  },
  {
    'type': 'section',
    'class': '',
    'header': 'Variant Publications',
    'anchor': 'Variant_Publications',
    'header_datasets': [],
    'props': {
      'attachmentDataset': 'Variant_Publications',
      'genomicAttachmentType': 'hgvs_variant',
    },
    'rows': [{
      'class': '',
      'datasets': [
        {
          'dataset': 'Variant_Publications',
          'genomicType': 'hgvs_variant',
          'type': 'images-dataset',
        },
      ],
    }],
  },
  {
    'type': 'section',
    'class': '',
    'header': 'Gene Homology/Multi-Sequence Alignment',
    'anchor': 'Gene_Homology',
    'header_datasets': [],
    'props': {
      'attachmentDataset': 'GeneHomology_Multi-SequenceAlignment',
      'genomicAttachmentType': 'hgvs_variant',
    },
    'rows': [{
      'class': '',
      'datasets': [
        {
          'dataset': 'GeneHomology_Multi-SequenceAlignment',
          'genomicType': 'hgvs_variant',
          'type': 'images-dataset',
        },
      ],
    }],
  },
  {
    'type': 'section',
    'class': '',
    'header': 'Human Gene Expression',
    'anchor': 'Human_Gene_Expression',
    'header_datasets': [],
    'props': {
      'attachmentDataset': 'Protein_Expression',
      'genomicAttachmentType': 'gene',
    },
    'rows': [{
      'class': '',
      'datasets': [
        {
          'dataset': 'Protein_Expression',
          'genomicType': 'gene',
          'type': 'images-dataset',
        },
      ],
    }],
  },
  {
    'type': 'section',
    'class': '',
    'header': 'Human Gene versus Protein Expression Profile',
    'anchor': 'Human_Gene_versus_Protein_Expression',
    'header_datasets': [],
    'props': {
      'attachmentDataset': 'Human_Gene_versus_Protein_Expression_Profile',
      'genomicAttachmentType': 'gene',
    },
    'rows': [{
      'class': '',
      'datasets': [
        {
          'dataset': 'Human_Gene_versus_Protein_Expression_Profile',
          'genomicType': 'gene',
          'type': 'images-dataset',
        },
      ],
    }],
  },
  {
    'type': 'section',
    'class': '',
    'header': 'Model System Expression Profiles',
    'anchor': 'Expression_Profiles',
    'header_datasets': [],
    'props': {
      'attachmentDataset': 'Model_System_Expression_Profiles',
      'genomicAttachmentType': 'gene',
    },
    'rows': [{
      'class': '',
      'datasets': [
        {
          'dataset': 'Model_System_Expression_Profiles',
          'genomicType': 'gene',
          'type': 'images-dataset',
        },
      ],
    }],
  },
  {
    'type': 'section',
    'class': '',
    'header': 'Orthology',
    'anchor': 'Orthology',
    'header_datasets': [],
    'props': {
      'attachmentDataset': 'Orthology',
      'genomicAttachmentType': 'gene',
    },
    'rows': [{
      'class': '',
      'datasets': [
        {
          'dataset': 'Orthology',
          'genomicType': 'gene',
          'type': 'images-dataset',
        },
      ],
    }],
  },
  {
    'type': 'section',
    'class': '',
    'header': 'Mus musculus (Mouse) Model System',
    'anchor': 'Mouse_Model',
    'header_datasets': [],
    'rows': [
      {
        'class': '',
        'datasets': [
          {
            'dataset': 'Model Systems - Mouse - Automated',
            'type': 'text-dataset',
            'props': {
              'label': 'Mouse - Automated',
            },
          },
        ],
      },
    ],
  },
  {
    'type': 'section',
    'class': '',
    'header': 'Rattus norvegicus (Rat) Model System',
    'anchor': 'Rat_Model',
    'header_datasets': [],
    'rows': [
      {
        'class': '',
        'datasets': [
          {
            'dataset': 'Model Systems - Rat',
            'type': 'text-dataset',
            'props': {
              'label': 'Rat',
            },
          },
        ],
      },
    ],
  },
  {
    'type': 'section',
    'class': '',
    'header': 'Danio rerio (Zebrafish) Model System',
    'anchor': 'Zebrafish_Model',
    'header_datasets': [],
    'rows': [
      {
        'class': '',
        'datasets': [
          {
            'dataset': 'Model Systems - Zebrafish - Automated',
            'type': 'text-dataset',
            'props': {
              'label': 'Zebrafish - Automated',
            },
          },
        ],
      },
    ],
  },
  {
    'type': 'section',
    'class': '',
    'header': 'C.-Elegans (Worm) Model System',
    'anchor': 'Worm_Model',
    'header_datasets': [],
    'rows': [
      {
        'class': '',
        'datasets': [
          {
            'dataset': 'Model Systems - C-Elegens - Automated',
            'type': 'text-dataset',
            'props': {
              'label': 'C-Elegens - Automated',
            },
          },
        ],
      },
    ],
  },
  {
    'type': 'section',
    'class': '',
    'header': 'Modelability',
    'anchor': 'Modelability',
    'header_datasets': [],
    'props': {
      'attachmentDataset': 'Modelability',
      'genomicAttachmentType': 'gene',
    },
    'rows': [{
      'class': '',
      'datasets': [
        {
          'dataset': 'Modelability',
          'genomicType': 'gene',
          'type': 'images-dataset',
        },
      ],
    }],
  },
  {
    'type': 'section',
    'class': '',
    'header': 'Druggability',
    'anchor': 'Druggability',
    'header_datasets': [],
    'props': {
      'attachmentDataset': 'Druggability',
      'genomicAttachmentType': 'gene',
    },
    'rows': [{
      'class': '',
      'datasets': [
        {
          'dataset': 'Druggability',
          'genomicType': 'gene',
          'type': 'images-dataset',
        },
      ],
    }],
  },
];
