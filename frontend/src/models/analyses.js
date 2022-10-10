import Requests from '@/requests.js';
export default {
  async all() {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'analysis/summary';
    return await Requests.get(baseUrl + urlQuery);
  },

  async getAnalysis(analysisName) {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'analysis/' + analysisName;
    return await Requests.get(baseUrl + urlQuery);
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

  async attachSupportingEvidence(analysisName, evidence) {
    let attachmentForm = null;
    let url = `/rosalution/api/analysis/${analysisName}/attach`;

    if (evidence.type == 'file') {
      attachmentForm = {
        'upload_file': evidence.data,
        'comments': evidence.comment ? evidence : '  ', /** Required for now, inserting empty string */
      };
      url += '/file';
    } else if ( evidence.type == 'link') {
      attachmentForm = {
        'link_name': evidence.name,
        'link': evidence.data,
        'comments': evidence.comment ? evidence : '  ', /** Required for now, inserting empty string */
      };
      url += '/link';
    }

    if (null == attachmentForm) {
      throw new Error(`Evidence attachment ${evidence} type is invalid.`);
    }

    return await Requests.postForm(url, attachmentForm);
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
            'dataset': 'Gene Description',
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
          // {
          //   'dataset': 'CADD',
          //   'type': 'score-dataset',
          //   'props': {
          //     'label': 'CADD Indel Raw',
          //     'minimum': -10,
          //     'maximum': 99,
          //     'bounds': {
          //       'lowerBounds': 0.9,
          //       'upperBounds': 1.33,
          //     },
          //     'cutoff': 15,
          //   },
          // },
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
    ],
  },
  {
    'type': 'section',
    'class': '',
    'header': 'Gene Homology/Multi-Sequence allignment',
    'anchor': 'Gene_Homology',
    'header_datasets': [],
    'rows': [],
  }, {
    'type': 'section',
    'class': '',
    'header': 'Protein Expression',
    'anchor': 'Protein_Expression',
    'header_datasets': [],
    'rows': [],
  }, {
    'type': 'section',
    'class': '',
    'header': 'Modelability',
    'anchor': 'Modelability',
    'header_datasets': [],
    'rows': [],
  }, {
    'type': 'section',
    'class': '',
    'header': 'Model Systems',
    'anchor': 'Model_Systems',
    'header_datasets': [],
    'rows': [],
  }, {
    'type': 'section',
    'class': '',
    'header': 'Druggability',
    'anchor': 'Druggability',
    'header_datasets': [],
    'rows': [],
  },
];
