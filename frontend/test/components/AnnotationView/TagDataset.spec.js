import {expect, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import DatasetLabel from '@/components/AnnotationView/DatasetLabel.vue';
import TagDataset from '@/components/AnnotationView/TagDataset.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';


/**
   * Creates a shallow mount for the vue component.
   * @param {Object} propsData Mocked props data
   * @return {Object} shallowMount to be used
   */
function getMountedComponent(propsData) {
  const defaultPropsData = {
    label: 'HPO',
    value: [
      'HP:0001270: Motor delay',
      'HP:0001419: X-linked recessive inheritance',
    ],
  };

  return shallowMount(TagDataset, {
    propsData: {...defaultPropsData, ...propsData},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
      },
    },
  });
}

describe('TagDataset.vue', () => {
  let wrapper;

  it('renders the label as expected', () => {
    wrapper = getMountedComponent();

    const labelWrapper = wrapper.findComponent(DatasetLabel);

    expect(labelWrapper.props('label')).to.equal('HPO');
  });

  it('renders the label as link when linkout is provided', () => {
    const linkout = 'https://hpo.jax.org/app/';
    wrapper = getMountedComponent({linkout});

    const labelWrapper = wrapper.findComponent(DatasetLabel);

    expect(labelWrapper.props('linkout')).to.equal(linkout);
  });

  it('does not render a label when none is provided', () => {
    wrapper = getMountedComponent({label: undefined});

    const labelWrapper = wrapper.findComponent(DatasetLabel);

    expect(labelWrapper.props('label')).to.be.undefined;
  });

  it('renders tags correctly for array values', () => {
    const testData = [
      'HP:0001270: Motor delay',
      'HP:0001419: X-linked recessive inheritance',
    ];
    wrapper = getMountedComponent({value: testData});

    const tags = wrapper.findAll('.tag');

    expect(tags.length).to.equal(testData.length);
    testData.forEach((value, index) => {
      expect(tags[index].text()).to.contains(value);
    });
  });

  it('renders as a linkout if its provided', () => {
    wrapper = getMountedComponent({linkout: 'http://hpo.jax.org/app/', value: undefined});
    const labelWrapper = wrapper.findComponent(DatasetLabel);

    expect(wrapper.exists()).to.be.true;
    expect(labelWrapper.props('linkout')).to.equal('http://hpo.jax.org/app/');
  });

  it('renders tags correctly for string values', () => {
    const delimiter = ';   ';
    const testData = 'HP:0001270: Motor delay;   ' +
    'HP:0001419: X-linked recessive inheritance;   ' +
    'HP:0001371: Flexion contracture';

    wrapper = getMountedComponent({value: testData, delimiter});

    const tags = wrapper.findAll('.tag');

    const expectedValues = testData.split(delimiter);
    expect(tags.length).to.equal(expectedValues.length);
    expectedValues.forEach((value, index) => {
      expect(tags[index].text()).to.contains(value);
    });
  });

  it('renders no tags if there are none provided', () => {
    wrapper = getMountedComponent({value: undefined});

    const tags = wrapper.findAll('.tag');
    expect(tags.length).is.equal(0);
  });
});
