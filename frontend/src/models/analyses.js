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
};


const annotationRenderingTemporary = [
  {
    'type': 'section',
    'class': '',
    'header': 'gene',
    'props': {
      'linkouts': [],
    },
    'rows': [
      {
        'class': '',
        'datasets': [
          {
            'dataset': 'Gene Description',
            'type': 'text-dataset',
          },
        ],
      }, {
        'class': '',
        'datasets': [
          {
            'dataset': 'OMIM',
            'type': 'text-dataset',
            'props': {
              'label': '',
              'EntrezGeneId': '',
              'url': 'https://www.omim.org/entry/{Entrez Gene Id}',
            },
          },
        ],
      }, {
        'class': '',
        'datasets': [
          {
            'dataset': 'HPO',
            'type': 'text-dataset',
            'props': {
              'label': 'OMIM',
              '': '',
              'url': 'https://hpo.jax.org/app/browse/search?q={gene}&navFilter=all',
            }
          },
        ],
      },
    ],
  },
  {
    'type': 'section',
    'class': '',
    'header': 'variant',
    'props': {
      'linkouts': [],
    },
    'rows': [
      {
        'class': '',
        'datasets': [
          {
            'dataset': 'CADD',
            'type': 'score-dataset',
            'props': {
              'label': 'CADD Indel Raw',
              'minimum': -10,
              'maximum': 99,
              'bounds': {
                'lowerBounds': 0.9,
                'upperBounds': 1.33,
              },
              'cutoff': 15,
            },
          },
          {
            'dataset': 'Phylop100',
            'type': 'score-dataset',
            'props': {
              'label': 'Phylop100',
            },
          },
        ],
      },
      {
        'class': '',
        'datasets': [
          {
            'dataset': 'GERP',
            'type': 'score-dataset',
            'props': {
              'label': 'GERP',
              'minimum': -13.1,
              'maximum': 6.54,
            },
          },
          {
            'dataset': 'Mappability',
            'type': 'score-dataset',
            'props': {
              'label': 'Mappability',
              'minimum': -13.1,
              'maximum': 6.54,
            },
          }],
      },
    ],
  }, {
    'type': 'section',
    'class': '',
    'header': 'Gene Homology/Multi-Sequence allignment',
    'props': {
      'linkouts': [],
    },
  }, {
    'type': 'section',
    'class': '',
    'header': 'Protein Expression',
    'props': {
      'linkouts': [],
    },
  }, {
    'type': 'section',
    'class': '',
    'header': 'Modelability',
    'props': {
      'linkouts': [],
    },
  }, {
    'type': 'section',
    'class': '',
    'header': 'Model Systems',
    'props': {
      'linkouts': [],
    },
  }, {
    'type': 'section',
    'class': '',
    'header': 'Druggability',
    'props': {
      'linkouts': [],
    },
  },
];
