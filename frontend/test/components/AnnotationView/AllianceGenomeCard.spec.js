import {describe, expect, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import AllianceGenomeCard from '@/components/AnnotationView/AllianceGenomeCard.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

import modelFixture from '../../__fixtures__/mockAllianceGenomeModels.json';

/**
 * helper function that shallow mounts and returns the rendered component
 * @param {propsData} propsData props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(propsData) {
  const defaultPropsData = {
    model: modelFixture['8.1.0<=,LMNA,fish'],
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
  describe.each([
    ['aliance genome 8.1.0<= (LMNA) fish,', '8.1.0<=,LMNA,fish'],
    ['aliance genome 8.2.0>= (LMNA) fish,', '8.2.0>=,LMNA,fish'],
    ['aliance genome 8.1.0<= (NUMB) mouse,', '8.1.0<=,NUMB,mouse'],
    ['aliance genome 8.2.0>= (NUMB) mouse,', '8.2.0>=,NUMB,mouse'],
  ])('Displays %s model card', (title, mockModelName) => {
    const expected = {
      '8.1.0<=,LMNA,fish': {
        'header': 'lmna<sup>bw25/bw25</sup>',
        'background': '[background:] involves: 129S4/SvJae * C57BL/6',
        'source': 'ZFIN',
      },
      '8.2.0>=,LMNA,fish': {
        'header': 'lmna<sup>bw25/bw25</sup>',
        'background': '',
        'source': 'ZFIN',
      },
      '8.1.0<=,NUMB,mouse': {
        'header': 'Numb<sup>tm1Zili</sup>/Numb<sup>tm1Zili</sup> Numbl<sup>tm1Zili</sup>/Numbl<sup>tm1Zili</sup>' +
          ' Tg(Mx1-cre)1Cgn/?',
        'background': '[background:] involves: 129/Sv * C57BL/6 * CBA',
        'source': 'MGI',
      },
      '8.2.0>=,NUMB,mouse': {
        'header': 'Numb<sup>tm1Zili</sup>/Numb<sup>tm1Zili</sup> Numbl<sup>tm1Zili</sup>/Numbl<sup>tm1Zili</sup>' +
          ' Tg(Mx1-cre)1Cgn/?',
        'background': '[background:] involves: 129/Sv * C57BL/6 * CBA',
        'source': 'MGI',
      },
    };
    it('animal model card title', () => {
      const mockModel = modelFixture[mockModelName];
      const wrapper = getMountedComponent({model: mockModel});
      const cardHeader = wrapper.find('[data-test=model-header]');

      expect(cardHeader.html()).to.include(expected[mockModelName]['header']);
    });

    it('animal model card background', () => {
      const mockModel = modelFixture[mockModelName];
      const wrapper = getMountedComponent({model: mockModel});
      const cardBackground = wrapper.find('[data-test=model-background]');

      expect(cardBackground.html()).to.include(expected[mockModelName]['background']);
    });

    it('animal model source', () => {
      const mockModel = modelFixture[mockModelName];
      const wrapper = getMountedComponent({model: mockModel});
      const modelSource = wrapper.find('[data-test=model-source]');

      expect(modelSource.html()).to.include(expected[mockModelName]['source']);
    });
  });

  describe.each([
    ['aliance genome 8.1.0<=', modelFixture['8.1.0<=,NUMB,mouse']],
    ['aliance genome 8.2.0>=', modelFixture['8.2.0>=,NUMB,mouse']],
  ])('animal models from %s are missing', (title, mockModelFixture) => {
    const expectedTitle = 'Numbtm1Zili/Numbtm1Zili Numbltm1Zili/Numbltm1Zili Tg(Mx1-cre)1Cgn/?';

    it('model conditions', () => {
      const wrapper = getMountedComponent({model: mockModelFixture});
      const cardHeader = wrapper.find('[data-test=model-header]');

      expect(cardHeader.text()).to.include(expectedTitle);
    });

    it('phenotypes', () => {
      const wrapper = getMountedComponent({model: mockModelFixture});
      const cardHeader = wrapper.find('[data-test=model-header]');

      expect(cardHeader.text()).to.include(expectedTitle);
    });

    it('diseases', () => {
      const wrapper = getMountedComponent({model: mockModelFixture});
      const diseasesList = wrapper.find('[data-test=model-list-disease]');

      expect(diseasesList.exists()).to.be.false;
    });
  });

  describe('card sections with lists render section header grey if list is empty, otherwise renders black', () => {
    it.each([
      ['aliance genome 8.1.0<=', modelFixture['8.1.0<=,NUMB,mouse'], '--rosalution-grey-300'],
      ['aliance genome 8.2.0>=', modelFixture['8.2.0>=,NUMB,mouse'], '--rosalution-grey-300'],
      ['aliance genome 8.1.0<=', modelFixture['8.1.0<=,LMNA,fish'], 'color: black;'],
      ['aliance genome 8.2.0>=', modelFixture['8.2.0>=,LMNA,fish'], '--rosalution-grey-300'],
    ])('%s for disease models', (title, mockModelFixture, expected) => {
      const wrapper = getMountedComponent({model: mockModelFixture});

      const diseasesSection = wrapper.find('[data-test=model-section-disease]');
      expect(diseasesSection.attributes().style).to.include(expected);
    });

    it.each([
      ['aliance genome 8.1.0<= (NUMB) mouse,', modelFixture['8.1.0<=,NUMB,mouse'], '--rosalution-grey-300'],
      ['aliance genome 8.2.0>= (NUMB) mouse,', modelFixture['8.2.0>=,NUMB,mouse'], '--rosalution-grey-300'],
      ['aliance genome 8.1.0<= (LMNA) fish,', modelFixture['8.1.0<=,LMNA,fish'], 'color: black;'],
      ['aliance genome 8.2.0>= (LMNA) fish,', modelFixture['8.2.0>=,LMNA,fish'], 'color: black;'],
      ['aliance genome 8.1.0<= (LMNA) mouse,', modelFixture['8.1.0<=,LMNA,mouse'], 'color: black;'],
    ])('%s for associated phenotypes', (title, mockModelFixture, expected) => {
      const wrapper = getMountedComponent({model: mockModelFixture});

      const phenotypesSection = wrapper.find('[data-test=model-section-phenotype]');
      expect(phenotypesSection.attributes().style).to.include(expected);
    });

    it.each([
      ['aliance genome 8.1.0<= mouse,', modelFixture['8.1.0<=,NUMB,mouse'], '--rosalution-grey-300'],
      ['aliance genome 8.2.0>= mouse,', modelFixture['8.2.0>=,NUMB,mouse'], '--rosalution-grey-300'],
      ['aliance genome 8.1.0<= fish,', modelFixture['8.1.0<=,LMNA,fish'], 'color: black;'],
      ['aliance genome 8.2.0>= fish,', modelFixture['8.2.0>=,LMNA,fish'], 'color: black;'],
    ])('%s for experimental condition', (title, mockModelFixture, expected) => {
      const wrapper = getMountedComponent({model: mockModelFixture});
      const experimentalConditionSection = wrapper.find('[data-test=model-section-condition]');

      expect(experimentalConditionSection.attributes().style).to.include(expected);
    });
  });

  describe.each([
    ['aliance genome 8.1.0<=', modelFixture['8.1.0<=,LMNA,fish']],
    ['aliance genome 8.2.0>=', modelFixture['8.2.0>=,LMNA,fish']],
  ])('card section content from %s', (title, mockModelFixture) => {
    it('displays Phenotype lists with frequent term sub-headers ', () => {
      const wrapper = getMountedComponent({model: mockModelFixture});
      const phenotypesList = wrapper.findAll('[data-test=model-list-phenotype]');

      const firstTerm = phenotypesList[0].find('span');
      const firstTermList = phenotypesList[0].findAll('li');

      expect(firstTerm.html()).to.include('abnormal');
      expect(firstTermList.length).to.equal(5);

      const secondTerm = phenotypesList[1].find('span');
      const secondTermIcon = phenotypesList[1].find('font-awesome-icon-stub');
      const secondTermList = phenotypesList[1].findAll('li');

      expect(secondTerm.html()).to.include('decreased');
      expect(secondTermIcon.attributes().icon).to.equal('arrow-down');
      expect(secondTermList.length).to.equal(4);
    });

    it('Shows a list of conditions under the experimental conditions section', () => {
      const wrapper = getMountedComponent({model: mockModelFixture});
      const experimentalSectionList = wrapper.findAll('[data-test=model-list-condition]');

      expect(experimentalSectionList.length).to.equal(1);
    });
  });
});
