import {describe, expect, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import AllianceGenomeCard from '@/components/AnnotationView/AllianceGenomeCard.vue';
import CardDataset from '@/components/AnnotationView/CardDataset.vue';

/**
    * Creates a shallow mount for the vue component.
    * @param {Object} propsData Mocked props data
    * @return {Object} shallowMount to be used
*/
function getMountedComponent(propsData) {
  const defaultPropsData = {
    value: [],
    dataSet: '',
  };

  return shallowMount(CardDataset, {
    props: {...defaultPropsData, ...propsData},
  });
}

describe('CardDataset.vue', () => {
  it('Should not render AllianceGenomicCards if the props are empty', () => {
    const wrapper = getMountedComponent();
    const findAllianceGenomeCards = wrapper.findAllComponents(AllianceGenomeCard);

    expect(findAllianceGenomeCards.length).to.equal(0);
  });

  it('Should render AllianceGenomicCards with the given props data', () => {
    const wrapper = getMountedComponent({value: fakeModels});
    const findAllianceGenomeCards = wrapper.findAllComponents(AllianceGenomeCard);

    expect(findAllianceGenomeCards.length).to.equal(3);
  });
});

const fakeModels = [
  {
    'id': 'ZFIN:ZDB-FISH-230123-3',
    'name': 'lmna<sup>ot300/ot300</sup>',
    'displayName': 'lmna<ot300/ot300>',
    'phenotypes': [],
    'url': 'https://zfin.org/ZDB-FISH-230123-3',
    'type': 'affected_genomic_model',
    'crossReference': null,
    'source': {
      'name': 'ZFIN',
      'url': null,
    },
    'diseaseAssociationType': null,
    'diseaseModels': [],
    'publicationEvidenceCodes': [],
    'conditions': {},
    'conditionModifiers': {},
    'alleles': [],
    'sequenceTargetingReagents': [],
    'species': {
      'name': 'Danio rerio',
      'shortName': 'Dre',
      'dataProviderFullName': 'Zebrafish Information Network',
      'dataProviderShortName': 'ZFIN',
      'commonNames': '[\'zebrafish\', \'fish\', \'dre\']',
      'taxonId': 'NCBITaxon:7955',
    },
  },
  {
    'id': 'ZFIN:ZDB-FISH-220613-4',
    'name': 'lmna<sup>bw25/bw25</sup>',
    'displayName': 'lmna<bw25/bw25>',
    'phenotypes': [],
    'url': 'https://zfin.org/ZDB-FISH-220613-4',
    'type': 'affected_genomic_model',
    'crossReference': null,
    'source': {
      'name': 'ZFIN',
      'url': null,
    },
    'diseaseAssociationType': null,
    'diseaseModels': [],
    'publicationEvidenceCodes': [],
    'conditions': {},
    'conditionModifiers': {},
    'alleles': [],
    'sequenceTargetingReagents': [],
    'species': null,
  },
  {
    'id': 'ZFIN:ZDB-FISH-230123-4',
    'name': 'lmna<sup>ot300/+</sup>',
    'displayName': 'lmna<ot300/+>',
    'phenotypes': [],
    'url': 'https://zfin.org/ZDB-FISH-230123-4',
    'type': 'affected_genomic_model',
    'crossReference': null,
    'source': {
      'name': 'ZFIN',
      'url': null,
    },
    'diseaseAssociationType': null,
    'diseaseModels': [],
    'publicationEvidenceCodes': [],
    'conditions': {},
    'conditionModifiers': {},
    'alleles': [],
    'sequenceTargetingReagents': [],
    'species': null,
  },
];
