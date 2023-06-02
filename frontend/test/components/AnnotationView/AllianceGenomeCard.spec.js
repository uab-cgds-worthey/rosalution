import {describe, expect, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import AllianceGenomeCard from '@/components/AnnotationView/AllianceGenomeCard.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

/**
 * helper function that shallow mounts and returns the rendered component
 * @param {propsData} propsData props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
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

  it('Displays the Experimental Condition section with black text because it has list items', () => {
    const wrapper = getMountedComponent();
    const experimentalSection = wrapper.find('[data-test=model-section-condition]');

    expect(experimentalSection.attributes().style).toContain('color: black;');
  });

  it('Shows a list of conditions under the experimental conditions section', () => {
    const wrapper = getMountedComponent();
    const experimentalSectionList = wrapper.findAll('[data-test=model-list-condition]');

    expect(experimentalSectionList.length).to.equal(1);
  });

  it('Shows the Associated Human Diseases as gray because it has list items', () => {
    const wrapper = getMountedComponent();
    const diseasesSection = wrapper.find('[data-test=model-section-disease]');

    expect(diseasesSection.attributes().style).toContain('color: black;');
  });

  it('Shows the Associated Human Diseases as gray because there are no list items', () => {
    const wrapper = getMountedComponent({model: fakeEmptyModelProp});
    const diseasesSection = wrapper.find('[data-test=model-section-disease]');

    expect(diseasesSection.attributes().style).toContain('--rosalution-grey-300');
  });

  it('Does not display a list as there are no diseases to show', () => {
    const wrapper = getMountedComponent({model: fakeEmptyModelProp});
    const diseasesList = wrapper.find('[data-test=model-list-disease]');

    expect(diseasesList.exists()).to.be.false;
  });

  it('Displays the Associated Phenotypes section with black text because it has list items', () => {
    const wrapper = getMountedComponent();
    const phenotypesSection = wrapper.find('[data-test=model-section-phenotype]');

    expect(phenotypesSection.attributes().style).toContain('color: black;');
  });

  it('Shows the Associated Phenotypes section as gray because there are no items', () => {
    const wrapper = getMountedComponent({model: fakeEmptyModelProp});
    const phenotypesSection = wrapper.find('[data-test=model-section-phenotype]');

    expect(phenotypesSection.attributes().style).toContain('--rosalution-grey-300');
  });

  it('Displays Phenotype lists with frequent term sub-headers ', () => {
    const wrapper = getMountedComponent({model: fakeModelProp});
    const phenotypesList = wrapper.findAll('[data-test=model-list-phenotype]');

    const firstTerm = phenotypesList[0].find('span');
    const firstTermList = phenotypesList[0].findAll('li');

    expect(firstTerm.html()).toContain('abnormal');
    expect(firstTermList.length).to.equal(5);

    const secondTerm = phenotypesList[1].find('span');
    const secondTermIcon = phenotypesList[1].find('font-awesome-icon-stub');
    const secondTermList = phenotypesList[1].findAll('li');

    expect(secondTerm.html()).toContain('decreased');
    expect(secondTermIcon.attributes().icon).to.equal('arrow-down');
    expect(secondTermList.length).to.equal(4);
  });

  it('Displays the source of the animal model', () => {
    const wrapper = getMountedComponent();
    const modelSource = wrapper.find('[data-test=model-source]');

    expect(modelSource.html()).toContain('ZFIN');
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
  'diseaseModels': [
    {
      'disease': {
        'id': 'DOID:10754',
        'name': 'otitis media',
        'url': 'http://www.disease-ontology.org/?id=DOID:10754',
      },
      'associationType': 'IS_MODEL_OF',
      'diseaseModel': 'otitis media',
    },
    {
      'disease': {
        'id': 'DOID:3911',
        'name': 'progeria',
        'url': 'http://www.disease-ontology.org/?id=DOID:3911',
      },
      'associationType': 'IS_MODEL_OF',
      'diseaseModel': 'progeria',
    },
  ],
  'publicationEvidenceCodes': [],
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

const fakeEmptyModelProp = {
  'id': 'ZFIN:ZDB-FISH-220613-4',
  'name': 'lmna<sup>bw25/bw25</sup>',
  'displayName': 'lmna<bw25/bw25>',
  'phenotypes': [],
  'source': {
    'name': 'ZFIN',
    'url': null,
  },
  'diseaseModels': [],
  'conditions': {},
  'conditionModifiers': {},
  'alleles': [],
  'sequenceTargetingReagents': [],
  'species': null,
};
