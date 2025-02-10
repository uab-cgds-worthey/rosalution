import {expect, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import ClinvarDataset from '@/components/AnnotationView/ClinvarDataset.vue';
import DatasetLabel from '@/components/AnnotationView/DatasetLabel.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

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
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
      },
    },
  });
}

describe('ClinVarDataset.vue', () => {
  let wrapper;

  it('renders the label as expected', () => {
    wrapper = getMountedComponent();

    const labelWrapper = wrapper.findComponent(DatasetLabel);
    expect(labelWrapper.props('label')).to.equal('ClinVar');
  });
});
