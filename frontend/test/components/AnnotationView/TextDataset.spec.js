import {expect, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import DatasetLabel from '@/components/AnnotationView/DatasetLabel.vue';
import TextDataset from '@/components/AnnotationView/TextDataset.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

/**
   * Creates a shallow mount for the vue component.
   * @param {Object} propsData Mocked props data
   * @return {Object} shallowMount to be used
   */
function getMountedComponent(propsData) {
  const defaultPropsData = {
    label: 'Diseases',
    value: 'Lymphoedema-cholestasis syndrome, Hennekam lymphangiectasia-lymphedema syndrome 1, Lymph vessel dysplasia',
  };

  return shallowMount(TextDataset, {
    propsData: {...defaultPropsData, ...propsData},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
      },
    },
  });
}

describe('TextDataset.vue', () => {
  let wrapper;

  it('renders the label as expected', () => {
    wrapper = getMountedComponent();

    const labelWrapper = wrapper.findComponent(DatasetLabel);
    expect(labelWrapper.props('label')).to.equal('Diseases');
  });

  it('renders text content as expected', () => {
    wrapper = getMountedComponent();

    expect(wrapper.html()).to.contains(
        'Lymphoedema-cholestasis syndrome, Hennekam lymphangiectasia-lymphedema syndrome 1, Lymph vessel dysplasia',
    );
  });
});
