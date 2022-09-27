import {expect, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import TextDataset from '@/components/AnnotationView/TextDataset.vue';

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
  });
}

describe('TextDataset.vue', () => {
  let wrapper;

  it('renders the label as expected', () => {
    wrapper = getMountedComponent();

    const textWrapper = wrapper.find('[data-test=text-label]');

    expect(textWrapper.html()).to.contains('Diseases');
  });

  it('does not render a label when none is provided', () => {
    wrapper = getMountedComponent({label: undefined});

    const textWrapper = wrapper.find('[data-test=text-label]');

    expect(textWrapper.exists()).to.not.be.true;
  });
});
