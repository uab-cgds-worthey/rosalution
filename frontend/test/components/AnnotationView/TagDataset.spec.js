import {expect, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';
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

    const labelWrapper = wrapper.find('.dataset-label');

    expect(labelWrapper.text()).to.contains('HPO');
  });

  it('renders the label as link when linkout is provided', () => {
    const linkout = 'https://hpo.jax.org/app/';
    wrapper = getMountedComponent({linkout});

    const labelLink = wrapper.find('.dataset-label');

    expect(labelLink.attributes('href')).to.equal(linkout);
  });

  it('does not render a label when none is provided', () => {
    wrapper = getMountedComponent({label: undefined});

    const labelWrapper = wrapper.find('.dataset-label');

    expect(labelWrapper.exists()).to.not.be.true;
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

  it('renders as unavailable if data not provided', () => {
    const localThis = {isDataUnavailable: true};

    expect(TagDataset.computed.dataAvailabilityColour.call(localThis)).to.equal('var(--rosalution-grey-300)');
  });

  it('renders as a linkout if its provided', () => {
    const localThis = {isDataUnavailable: false, linkout: 'http://hpo.jax.org/app/'};

    expect(TagDataset.computed.dataAvailabilityColour.call(localThis)).to.equal('var(--rosalution-purple-300)');
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
      expect(tags[index].text()).to.contains(value.trim());
    });
  });
});
