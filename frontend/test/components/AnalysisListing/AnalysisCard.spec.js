import {expect, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';
// import {expect} from 'chai';

import AnalysisCard from '@/components/AnalysisListing/AnalysisCard.vue';

/**
 * helper function that mounts and returns the rendered component
 * @param {propsData} propsData render the analysis card component with
 * @return {Wrapper} returns a shallow mounted analysis card component with props data
 */
function getMountedComponent(propsData) {
  const defaultPropsData = {
    id: '10f7aa04-6adf-4538-a700-ebe2f519473f',
    name: 'CPAM0046',
    description: ': LMNA-related congenital muscular dystropy',
    genomic_units: [
      {gene: 'LMNA'},
      {transcript: 'NM_170707.3'},
      {chromosome: '1', position: '156134885', reference: 'C', alternate: 'T'},
    ],
    nominated_by: 'Dr. Person Two',
    latest_status: 'Approved',
    created_date: '2021-09-30',
    last_modified_date: '2021-10-01',
  };

  return shallowMount(AnalysisCard, {
    propsData: {...defaultPropsData, ...propsData},
  });
}

describe('AnalysisCard.vue', () => {
  it('should show the analysis name', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.html()).to.contains('CPAM0046');
  });

  it('should show when the case was created', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.html()).to.contains('2021-09-30');
  });

  it('should show the date a sample in the case was last modified', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.text()).to.contains('2021-10-01');
  });

  it('should show the nominator information of the case', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.html()).to.contains('Dr. Person Two');
  });

  describe('should show the genomic units of the case', () => {
    it('should show the gene information for a case', () => {
      const wrapper = getMountedComponent();
      expect(wrapper.html()).to.contains('Gene');
      expect(wrapper.html()).to.contains('LMNA');
    });
    it('should show the transcript information for a case', () => {
      const wrapper = getMountedComponent();
      expect(wrapper.html()).to.contains('Transcript');
      expect(wrapper.html()).to.contains('NM_170707.3');
    });
    it('should show the coordinates information for a case', () => {
      const wrapper = getMountedComponent();
      expect(wrapper.html()).to.contains('Chr1:156134885 C>T');
    });
  });
});
