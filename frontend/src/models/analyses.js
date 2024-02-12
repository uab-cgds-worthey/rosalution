import {EventType} from '@/enums.js';
import Requests from '@/requests.js';

export default {

  EventType,

  async all() {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'analysis/summary';
    const analysesSummary = await Requests.get(baseUrl + urlQuery);
    return analysesSummary;
  },

  async getSummaryByName(analysisName) {
    const url = `/rosalution/api/analysis/${analysisName}/summary`;
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

  /**
   * Provides {@link updatedSections} of updated text fields within sections in
   * the analysis {@link analysisName}.
   * @param {string} analysisName The unique name of the Analysis to update
   * @param {Object} updatedSections The list of updated fields from within
   *                                 their corresponding sections
   * @return {Object[]} Array of all of the sections, including the updated
   * ones, within the Analysis
   */
  async updateAnalysisSections(analysisName, updatedSections) {
    const sectionsToUpdate = [];
    for (const [sectionName, field] of Object.entries(updatedSections)) {
      const analysisSection = {
        header: sectionName,
        content: [],
      };

      for ( const [fieldName, fieldValue] of Object.entries(field)) {
        analysisSection.content.push({
          fieldName: fieldName,
          value: fieldValue,
        });
      }
      sectionsToUpdate.push(analysisSection);
    }
    const url = `/rosalution/api/analysis/${analysisName}/sections/batch`;
    return await Requests.post(url, sectionsToUpdate);
  },

  async pushAnalysisEvent(analysisName, eventType) {
    const url = `/rosalution/api/analysis/${analysisName}/event/${eventType}`;
    return await Requests.put(url);
  },

  async getAnnotationConfiguration(analysisName) {
    // const baseUrl = '/rosalution/api/';
    // const urlQuery = `analysis/{analysisName}`;

    return annotationRenderingTemporary;
  },

  /**
   * Requests to upload the JSON required for creating a new analysis in Rosalution
   * with a unique analysis name.
   * @param {File} file The JSON for creating the new Analysis
   * @return {Object} Returns the new complete analysis created within Rosalution
   */
  async importPhenotipsAnalysis(file) {
    const url = '/rosalution/api/analysis';

    const fileUploadFormData = {
      'phenotips_file': file,
    };

    return Requests.postForm(url, fileUploadFormData);
  },

  async getSectionImage(fileId) {
    const url = `/rosalution/api/analysis/download/${fileId}`;
    return await Requests.getImage(url);
  },

  /**
   * Attaches {@link image} to {@link field} within {@link sectionName}
   * the analysis {@link analysisName}.
   * @param {string} analysisName The unique name of the analysis to update
   * @param {string} sectionName The name of the section within the analysis
   * @param {string} field The identifiying field within the section
   * @param {File}   image the image data to be uploaded
   * @return {Object} Returns the updated field with the image attachment id
   */
  async attachSectionImage(analysisName, sectionName, field, image) {
    const url = `/rosalution/api/analysis/${analysisName}/sections?row_type=image`;

    const section = {
      'header': sectionName,
      'content': [],
    };
    section.content.push({
      'fieldName': field,
    });
    const attachmentForm = {
      'upload_file': image,
      'updated_section': JSON.stringify(section),
    };

    const updatedAnalysisSections = await Requests.postForm(url, attachmentForm);

    return updatedAnalysisSections.find((section) => {
      return section.header == sectionName;
    })?.content.find((row) => {
      return row.field == field;
    });
  },

  async updateSectionImage(analysisName, sectionName, field, oldFileId, image) {
    const section = {
      'header': sectionName,
      'content': [],
    };
    section.content.push({
      'fieldName': field,
    });
    const attachmentForm = {
      'upload_file': image,
      'updated_section': JSON.stringify(section),
    };

    const url = `/rosalution/api/analysis/${analysisName}/sections/${oldFileId}?row_type=image`;

    const updatedAnalysisSections = await Requests.putForm(url, attachmentForm);

    return updatedAnalysisSections.find((section) => {
      return section.header == sectionName;
    })?.content.find((row) => {
      return row.field == field;
    });
  },

  async removeSectionAttachment(analysisName, sectionName, fieldName, oldSectionAttachmentId) {
    const url = `/rosalution/api/analysis/${analysisName}/sections/${oldSectionAttachmentId}`;
    const updatedSections = await Requests.delete(url);
    return updatedSections.find((section) => {
      return section.header == sectionName;
    })?.content.find((row) => {
      return row.field == fieldName;
    });
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

  async attachSectionSupportingEvidence(analysisName, sectionName, field, evidence) {
    let attachmentForm = null;
    let url = `/rosalution/api/analysis/${analysisName}/sections?row_type=`;

    const section = {
      'header': sectionName,
      'content': [],
    };

    if (evidence.type == 'file') {
      section.content.push({
        'fieldName': field,
      });

      attachmentForm = {
        'upload_file': evidence.data,
        'updated_section': JSON.stringify(section),
      };

      url += 'document';
    } else if ( evidence.type == 'link') {
      section.content.push({
        'fieldName': field,
        'linkName': evidence.name,
        'link': evidence.data,
      });

      attachmentForm = {
        'updated_section': JSON.stringify(section),
      };

      url += 'link';
    }

    if (null == attachmentForm) {
      throw new Error(`Evidence attachment ${evidence} type is invalid.`);
    }

    const updatedSections = await Requests.postForm(url, attachmentForm);
    return updatedSections.find((section) => {
      return section.header == sectionName;
    })?.content.find((row) => {
      return row.field == field;
    });
  },
  async postNewDiscussionThread(analysisName, postContent) {
    const url = `/rosalution/api/analysis/${analysisName}/discussions`;

    const attachmentForm = {
      'discussion_content': postContent,
    };

    const success = await Requests.postForm(url, attachmentForm);
    return success;
  },
  async editDiscussionThreadById(analysisName, postId, postContent) {
    const url = `/rosalution/api/analysis/${analysisName}/discussions/${postId}`;

    const attachmentForm = {'discussion_content': postContent};

    const success = await Requests.putForm(url, attachmentForm);

    return success;
  },
  async deleteDiscussionThreadById(analysisName, postId) {
    const url = `/rosalution/api/analysis/${analysisName}/discussions/${postId}`;

    const success = await Requests.delete(url);

    return success;
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
            'type': 'tag-dataset',
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
              'minimum': 0,
              'maximum': 99,
              'bounds': {
                'lowerBound': 9,
                'upperBound': 19,
              },
              'cutoff': 1,
            },
          },
          {
            'dataset': 'DITTO',
            'type': 'score-dataset',
            'props': {
              'label': 'DITTO',
              'minimum': 0,
              'maximum': 1,
              'bounds': {
                'lowerBound': 0.5,
                'upperBound': 0.79,
              },
              'cutoff': 1,
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
    'header_datasets': [
      {
        'dataset': 'GTEx_Human_Gene_Expression_url',
        'type': 'icon-linkout-dataset',
        'props': {
          'imageFilename': 'gtex_logo.png',
          'altText': 'GTEx Human Gene Expression URL',
        },
      },
    ],
    'props': {
      'attachmentDataset': 'Human_Gene_Expression',
      'genomicAttachmentType': 'gene',
    },
    'rows': [{
      'class': '',
      'datasets': [
        {
          'dataset': 'Human_Gene_Expression',
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
    'header_datasets': [
      {
        'dataset': 'Human_Protein_Atlas_Protein_Gene_Search_url',
        'type': 'icon-linkout-dataset',
        'props': {
          'imageFilename': 'protein_atlas_icon.png',
          'altText': 'Protein Atlas Gene Search URL',
        },
      },
    ],
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
    'header_datasets': [
      {
        'dataset': 'CoSIA_url',
        'type': 'icon-linkout-dataset',
        'props': {
          'imageFilename': 'CoSIA_logo.png',
          'altText': 'COSIA_LINKOUT',
          'value': 'https://lasseignelab.shinyapps.io/CoSIA/',
        },
      },
      {
        'dataset': 'Frog_General_Xenbase_Database_url',
        'type': 'icon-linkout-dataset',
        'props': {
          'imageFilename': 'xenbase_logo.png',
          'altText': 'Xenbase Xenopus General Gene Linkout',
        },
      },
    ],
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
    'header_datasets': [{
      'dataset': 'Human_Alliance_Genome_url',
      'type': 'icon-linkout-dataset',
      'props': {
        'imageFilename': 'alliance-genome-logo.png',
        'altText': 'Human Alliance Genome Linkout',
      },
    }],
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
    'header': 'Rattus norvegicus (Rat) Model System',
    'anchor': 'Rattus_norvegicus_Model_System',
    'header_datasets': [
      {
        'dataset': 'Rat_Alliance_Genome_url',
        'type': 'icon-linkout-dataset',
        'props': {
          'imageFilename': 'alliance-genome-logo.png',
          'altText': 'Alliance Genome Linkout',
        },
      }, {
        'dataset': 'Rat_Rat_Genome_Database_url',
        'type': 'icon-linkout-dataset',
        'props': {
          'imageFilename': 'rat-dataset-logo.png',
          'altText': 'Rat Genome Database Linkout',
        },
      },
    ],
    'rows': [{
      'class': '',
      'datasets': [
        {
          'dataset': 'Rat_Alliance_Genome_Automated_Summary',
          'type': 'text-dataset',
          'props': {
            'label': 'AG Summary',
          },
        },
        {
          'dataset': 'Rat_Alliance_Genome_RGD_Summary',
          'type': 'text-dataset',
          'props': {
            'label': 'RGD Summary',
          },
        },
        {
          'dataset': 'Rat_Alliance_Genome_Models',
          'type': 'card-dataset',
        },
      ],
    }],
  },
  {
    'type': 'section',
    'class': '',
    'header': 'Mus musculus (Mouse) Model System',
    'anchor': 'Mus_musculus_Model_System',
    'header_datasets': [
      {
        'dataset': 'Mouse_Alliance_Genome_url',
        'type': 'icon-linkout-dataset',
        'props': {
          'imageFilename': 'alliance-genome-logo.png',
          'altText': 'Alliance Genome Linkout',
        },
      }, {
        'dataset': 'Mouse_Mouse_Genome_Database_url',
        'type': 'icon-linkout-dataset',
        'props': {
          'imageFilename': 'mouse-dataset-logo.png',
          'altText': 'Mouse Genome Informatics Linkout',
        },
      },
    ],
    'rows': [{
      'class': '',
      'datasets': [
        {
          'dataset': 'Mouse_Alliance_Genome_Automated_Summary',
          'type': 'text-dataset',
          'props': {
            'label': 'AG Summary',
          },
        },
        {
          'dataset': 'Mouse_Alliance_Genome_MGI_Summary',
          'type': 'text-dataset',
          'props': {
            'label': 'MGI Summary',
          },
        },
        {
          'dataset': 'Mouse_Alliance_Genome_Models',
          'type': 'card-dataset',
        },
      ],
    }],
  },
  {
    'type': 'section',
    'class': '',
    'header': 'Danio rerio (Zebrafish) Model System',
    'anchor': 'Danio_rerio_Model_System',
    'header_datasets': [
      {
        'dataset': 'Zebrafish_Alliance_Genome_url',
        'type': 'icon-linkout-dataset',
        'props': {
          'imageFilename': 'alliance-genome-logo.png',
          'altText': 'Alliance Genome Linkout',
        },
      }, {
        'dataset': 'Zebrafish_Zebrafish_Information_Network_url',
        'type': 'icon-linkout-dataset',
        'props': {
          'imageFilename': 'zebrafish-dataset-logo.png',
          'altText': 'Zebrafish Information Network Linkout',
        },
      },
    ],
    'rows': [{
      'class': '',
      'datasets': [
        {
          'dataset': 'Zebrafish_Alliance_Genome_Automated_Summary',
          'type': 'text-dataset',
          'props': {
            'label': 'AG Summary',
          },
        },
        {
          'dataset': 'Zebrafish_Alliance_Genome_ZFIN_Summary',
          'type': 'text-dataset',
          'props': {
            'label': 'ZFIN Summary',
          },
        },
        {
          'dataset': 'Zebrafish_Alliance_Genome_Models',
          'type': 'card-dataset',
        },
      ],
    }],
  },
  {
    'type': 'section',
    'class': '',
    'header': 'C. elegans (Roundworm) Model System',
    'anchor': 'C_elegans_Model_System',
    'header_datasets': [
      {
        'dataset': 'C-Elegens_Alliance_Genome_url',
        'type': 'icon-linkout-dataset',
        'props': {
          'imageFilename': 'alliance-genome-logo.png',
          'altText': 'Alliance Genome Linkout',
        },
      }, {
        'dataset': 'C-Elegens_Worm_Base_url',
        'type': 'icon-linkout-dataset',
        'props': {
          'imageFilename': 'c-elegens-dataset-logo.png',
          'altText': 'WormBase Linkout',
        },
      },
    ],
    'rows': [{
      'class': '',
      'datasets': [
        {
          'dataset': 'C-Elegens_Alliance_Genome_Automated_Summary',
          'type': 'text-dataset',
          'props': {
            'label': 'AG Summary',
          },
        },
        {
          'dataset': 'C-Elegens_Alliance_Genome_WB_Summary',
          'type': 'text-dataset',
          'props': {
            'label': 'WB Summary',
          },
        },
        {
          'dataset': 'C-Elegens_Alliance_Genome_Models',
          'type': 'card-dataset',
        },
      ],
    }],
  },
  {
    'type': 'section',
    'class': '',
    'header': 'Modelability',
    'anchor': 'Modelability',
    'header_datasets': [
      {
        'dataset': 'Gentar_url',
        'type': 'icon-linkout-dataset',
        'props': {
          'imageFilename': 'gentar_logo.png',
          'altText': 'Gentar URL for Modelability',
          'value': 'https://www.gentar.org/',
        },
      },
    ],
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
    'header_datasets': [{
      'dataset': 'Pharos_Target_url',
      'type': 'icon-linkout-dataset',
      'props': {
        'imageFilename': 'pharos_logo.png',
        'altText': 'Druggability Target in Pharos',
      },
    }],
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
