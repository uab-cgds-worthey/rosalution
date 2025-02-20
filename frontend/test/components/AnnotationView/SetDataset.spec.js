import {expect, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import DatasetLabel from '@/components/AnnotationView/DatasetLabel.vue';
import SetDataset from '@/components/AnnotationView/SetDataset.vue';

/**
   * Creates a shallow mount for the vue component
   * @param {Object} propsData Mocked props data
   * @return {Object} shallowMount to be used
   */
function getMountedComponent(propsData) {
  const defaultPropsData = {
    label: 'PROVEAN',
    value: 'D',
    set: [{value: 'B', classification: 'Benign', colour: 'Blue'},
      {value: 'P', classification: 'Possibly Damaging', colour: 'Yellow'},
      {value: 'D', classification: 'Probably Damaging', colour: 'Red'},
      {value: 'R', classification: 'Really Damaging', colour: 'Green'},
    ],
    ticker: true,
  };

  return shallowMount(SetDataset, {
    propsData: {...defaultPropsData, ...propsData},
  });
}

describe('SetDataset.vue', () => {
  it('renders a label with the value', () => {
    const wrapper = getMountedComponent();

    const labelWrapper = wrapper.findComponent(DatasetLabel);
    expect(labelWrapper.props('label')).to.equal('PROVEAN');
  });

  it('renders as unavailable if data does not exist', () => {
    const wrapper = getMountedComponent({
      value: '.',
    });

    const setUnavailable = wrapper.find('[data-test=dataset-bar]');
    expect(setUnavailable.classes()).to.contain('dataset-bar-fill-unavailable');
  });

  it('renders each item in a set', () => {
    const wrapper = getMountedComponent();

    const datasetBar = wrapper.find('[data-test=dataset-bar]');
    const setItems = datasetBar.findAll('span');
    expect(setItems.length).to.equal(4);
  });

  it('renders each item in a set with different background colours', () => {
    const wrapper = getMountedComponent();

    const datasetBar = wrapper.find('[data-test=dataset-bar]');
    const setItems = datasetBar.findAll('span');

    const backgroundColours = setItems
        .map((item)=> {
          return item.attributes()
              .style
              .split(' ')
              .filter( (attr) => attr.includes('var'));
        });
    const distinctBackgroundColours = [...new Set(backgroundColours)];
    expect(distinctBackgroundColours).to.have.lengthOf(4);
  });

  it('renders the value as the prominent item in the dataset', () => {
    const wrapper = getMountedComponent({
      value: 'R',
    });

    const datasetBar = wrapper.find('[data-test=dataset-bar]');
    const setItems = datasetBar.findAll('span');

    const fourthClassification = setItems.filter(function(item) {
      return !(item.text() === '');
    });
    expect(fourthClassification[0].text()).to.equal('Really Damaging');
  });

  it('renders set items not the value are not prominent', () => {
    const wrapper = getMountedComponent({
      value: 'R',
    });

    const datasetBar = wrapper.find('[data-test=dataset-bar]');
    const setItems = datasetBar.findAll('span');
    setItems.forEach((item) => {
      if (item.text() != 'Really Damaging') {
        expect(item.attributes().style).to.include('opacity: 0.5');
      }
    });
  });
});
