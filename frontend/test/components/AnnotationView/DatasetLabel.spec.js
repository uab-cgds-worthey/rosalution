import {expect, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import DatasetLabel from '@/components/AnnotationView/DatasetLabel.vue';
 
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

/**
   * Creates a shallow mount for the vue component.
   * @param {Object} propsData Mocked props data
   * @return {Object} shallowMount to be used
   */
function getMountedComponent(propsData) {
  const defaultPropsData = {
    label: 'Diseases',
    datasetValue: 'Lymphoedema-cholestasis syndrome, Hennekam lymphangiectasia-lymphedema syndrome 1, Lymph vessel dysplasia',
  };

  return shallowMount(DatasetLabel, {
    propsData: {...defaultPropsData, ...propsData},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
      },
    },
  });
}

describe('DatasetLabel.vue', () => {
  let wrapper;

  it('renders the label as expected', () => {
    wrapper = getMountedComponent();

    expect(wrapper.html()).to.contains('Diseases');
  });

  it('renders as available when data is available', () => {
    wrapper = getMountedComponent();

    expect(wrapper.attributes('style')).to.contain('black');
  });

  it('renders linkout as expected', () => {
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

    expect(wrapper.classes()).to.be.empty;
    expect(wrapper.text()).to.equal('');
  });

  it('renders as unavailable if data not provided', () => {
    [undefined, ""].forEach((undefinedValue) => {
      wrapper = getMountedComponent({datasetValue: undefinedValue});
      expect(wrapper.attributes('style')).to.contain('annotation-dataset-unavailable');
    })
  });

  it('renders as a linkout if its provided', () => {
    wrapper = getMountedComponent({datasetValue: undefined, linkout: 'http://sites.uab.edu/cgds'});
    const labelLinkout = wrapper.find('a');
    expect(labelLinkout.exists()).to.be.true;
  });
});
