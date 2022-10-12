import {expect, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import ClinvarDataset from '@/components/AnnotationView/ClinvarDataset.vue';

/**
   * Creates a shallow mount for the vue component.
   * @param {Object} propsData Mocked props data
   * @return {Object} shallowMount to be used
   */
function getMountedComponent(propsData) {
  const defaultPropsData = {
    label: 'ClinVar',
    linkout: 'https://sites.uab.edu/cgds/',
  };

  return shallowMount(ClinvarDataset, {
    propsData: {...defaultPropsData, ...propsData},
  });
}

describe('ClinVarDataset.vue', () => {
  let wrapper;

  it('renders the label as expected', () => {
    wrapper = getMountedComponent();

    const textWrapper = wrapper.find('[data-test=text-label]');

    expect(textWrapper.html()).to.contains('ClinVar');
  });

  it('renders the label as expected', () => {
    wrapper = getMountedComponent();

    const labelLinkout = wrapper.find('a');

    expect(labelLinkout.html()).to.contains('ClinVar');
    expect(labelLinkout.attributes('href')).to.equal('https://sites.uab.edu/cgds/');
    expect(labelLinkout.attributes('target')).to.equal('_blank');
  });
});
