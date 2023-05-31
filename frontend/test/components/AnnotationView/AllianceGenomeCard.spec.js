import {describe, expect, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import AllianceGenomeCard from '@/components/AnnotationView/AllianceGenomeCard.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

function getMountedComponent(propsData) {
  const defaultPropsData = {
    model: fakeModelProp,
  };

  return shallowMount(AllianceGenomeCard, {
    props: {...defaultPropsData, ...propsData},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
      },
    },
  });
}

describe('AllianceGenomeCard.vue', () => {
  it('Displays a card with the proper title', () => {
    const wrapper = getMountedComponent();
    const cardHeader = wrapper.find('[data-test=model-header]');

    expect(cardHeader.html()).toContain('lmna<sup>bw25/bw25</sup>');
  });

  it('Displays a card with a proper background', () => {
    const wrapper = getMountedComponent();
    const cardBackground = wrapper.find('[data-test=model-background]');

    expect(cardBackground.html()).toContain('[background:] involves: 129S4/SvJae * C57BL/6');
  });

  it('Displays the Experimental Condition section with black text because it has a property', () => {
    const wrapper = getMountedComponent();
    const experimentalSection = wrapper.find('[data-test=model-section-condition]');

    expect(experimentalSection.attributes().style).toContain('color: black;');
  });
});

const fakeModelProp = {
  'id': 'ZFIN:ZDB-FISH-220613-4',
  'name': 'lmna<sup>bw25/bw25</sup> [background:] involves: 129S4/SvJae * C57BL/6',
  'displayName': 'lmna<bw25/bw25>',
  'phenotypes': [
    'atrioventricular canal cardiac conduction decreased process quality, abnormal',
    'cardiac muscle cell nucleus morphology, abnormal',
    'cardiac ventricle cardiac conduction decreased process quality, abnormal',
    'heart contraction decreased rate, abnormal',
    'heart decreased functionality, abnormal',
  ],
  'url': 'https://zfin.org/ZDB-FISH-220613-4',
  'type': 'affected_genomic_model',
  'crossReference': null,
  'source': {
    'name': 'ZFIN',
    'url': null,
  },
  'diseaseAssociationType': null,
  'diseaseModels': [],
  'publicationEvidenceCodes': [
    {
      'primaryKey': '0d26b7d9-dc2d-4022-8630-7c18c4ec169e',
      'publication': {
        'id': 'PMID:31977013',
        'url': 'https://www.ncbi.nlm.nih.gov/pubmed/31977013',
      },
      'dateAssigned': null,
      'evidenceCodes': [],
    },
    {
      'primaryKey': '9a017502-cf7e-4525-b842-9c85f326ae9e',
      'publication': {
        'id': 'PMID:31977013',
        'url': 'https://www.ncbi.nlm.nih.gov/pubmed/31977013',
      },
      'dateAssigned': null,
      'evidenceCodes': [],
    },
    {
      'primaryKey': '48abf479-3482-449e-8cf0-df631aa37cb3',
      'publication': {
        'id': 'PMID:31977013',
        'url': 'https://www.ncbi.nlm.nih.gov/pubmed/31977013',
      },
      'dateAssigned': null,
      'evidenceCodes': [],
    },
    {
      'primaryKey': '1624fc58-153f-419f-80ef-2e094fe1e0b8',
      'publication': {
        'id': 'PMID:31977013',
        'url': 'https://www.ncbi.nlm.nih.gov/pubmed/31977013',
      },
      'dateAssigned': null,
      'evidenceCodes': [],
    },
    {
      'primaryKey': '6e8a385e-0501-4949-a768-76c898aff653',
      'publication': {
        'id': 'PMID:31977013',
        'url': 'https://www.ncbi.nlm.nih.gov/pubmed/31977013',
      },
      'dateAssigned': null,
      'evidenceCodes': [],
    },
  ],
  'conditions': {
    'has_condition': [
      {
        'primaryKey': 'standard conditionsZECO:0000103',
        'conditionStatement': 'standard conditions',
        'term': {
          'id': 'ZECO:0000103',
          'name': 'standard conditions',
        },
      },
    ],
  },
  'conditionModifiers': {},
  'alleles': [],
  'sequenceTargetingReagents': [],
  'species': null,
};
