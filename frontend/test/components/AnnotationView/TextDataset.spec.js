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

  it('renders the label as expected', () => {
    wrapper = getMountedComponent({
      linkout: 'https://sites.uab.edu/cgds/',
    });

    const labelLinkout = wrapper.find('a');

    expect(labelLinkout.html()).to.contains('Diseases');
    expect(labelLinkout.attributes('href')).to.equal('https://sites.uab.edu/cgds/');
    expect(labelLinkout.attributes('target')).to.equal('_blank');
  });

  it('does not render a label when none is provided', () => {
    wrapper = getMountedComponent({label: undefined});

    const textWrapper = wrapper.find('[data-test=text-label]');

    expect(textWrapper.exists()).to.not.be.true;
  });

  it('renders as unavailable if data not provided', () => {
    const localThis = {isDataUnavailable: true};

    expect(TextDataset.computed.dataAvailabilityColour.call(localThis)).to.equal('var(--rosalution-grey-300)');
  });

  it('renders as a linkout if its provided', () => {
    const localThis = {isDataUnavailable: false, linkout: 'http://sites.uab.edu/cgds'};

    expect(TextDataset.computed.dataAvailabilityColour.call(localThis)).to.equal('var(--rosalution-purple-300)');
  });
});
