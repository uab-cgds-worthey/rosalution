import {expect, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import ScoreDataset from '@/components/AnnotationView/ScoreDataset.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

/**
   * Creates a shallow mount for Score Dataset component.
   * @param {Object} propsData Mocked props data
   * @return {Object} shallowMount to be used
   */
function getMountedComponent(propsData) {
  const defaultPropsData = {
    label: 'CADD_phred',
    value: 9,
    minimum: 0,
    maximum: 99,
    bounds: {
      upperBound: 1.33,
      lowerBound: .9,
    },
    cutoff: 15,
  };

  return shallowMount(ScoreDataset, {
    propsData: {...defaultPropsData, ...propsData},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
      },
    },
  });
}

describe('ScoreDataset.vue', () => {
  let wrapper;
  it('renders the dataset label', () => {
    wrapper = getMountedComponent();
    expect(wrapper.html()).to.contain('CADD_phred');
  });

  describe('when a score is set', () => {
    describe('with a positive range', () => {
      it('shows a nominal score component', () => {
        wrapper = getMountedComponent();

        const scoreFill = wrapper.find('[data-test=score-fill]');
        expect(scoreFill.attributes().style).to.contain('');
        expect(scoreFill.attributes().style).to.contains('width: 9%;');

        const scoreBackground = wrapper.find('[data-test=score-background]');
        expect(scoreBackground.attributes().style).to.contain('rosalution-blue-300');

        const scoreText = wrapper.find('[data-test=score-text]');
        expect(scoreText.attributes().style).to.contain('rosalution-blue-300');
        expect(scoreText.text()).to.equal('9');
      });

      it('shows a borderline score component', () => {
        wrapper = getMountedComponent({
          value: '15',
        });

        const scoreFill = wrapper.find('[data-test=score-fill]');
        expect(scoreFill.attributes().style).to.contain('rosalution-yellow-200');
        expect(scoreFill.attributes().style).to.contains('width: 15%;');

        const scoreBackground = wrapper.find('[data-test=score-background]');
        expect(scoreBackground.attributes().style).to.contain('rosalution-yellow-300');

        const scoreText = wrapper.find('[data-test=score-text]');
        expect(scoreText.attributes().style).to.contain('rosalution-yellow-300');
        expect(scoreText.text()).to.equal('15');
      });

      it('shows a critical score component', () => {
        wrapper = getMountedComponent({
          value: '22.2',
        });
        const scoreFill = wrapper.find('[data-test=score-fill]');
        expect(scoreFill.attributes().style).to.contains('rosalution-red-200');
        expect(scoreFill.attributes().style).to.contains('width: 22%;');

        const scoreBackground = wrapper.find('[data-test=score-background]');
        expect(scoreBackground.attributes().style).to.contains('rosalution-red-300');

        const scoreText = wrapper.find('[data-test=score-text]');
        expect(scoreText.attributes().style).to.contains('rosalution-red-300');
        expect(scoreText.text()).to.equal('22.2');
      });
    });

    describe('with a range that spans a negative value', () => {
      it('shows a nominal value', () => {
        wrapper = getMountedComponent({
          value: 15,
          minimum: -10,
          maximum: 99,
          bounds: {
            upperBound: 2,
            lowerBound: 1,
          },
        });

        const scoreFill = wrapper.find('[data-test=score-fill]');
        expect(scoreFill.attributes().style).to.contain('rosalution-blue-200');
        expect(scoreFill.attributes().style).to.contains('width: 22%;');

        const scoreBackground = wrapper.find('[data-test=score-background]');
        expect(scoreBackground.attributes().style).to.contain('rosalution-blue-300');

        const scoreText = wrapper.find('[data-test=score-text]');
        expect(scoreText.attributes().style).to.contain('rosalution-blue-300');
        expect(scoreText.text()).to.equal('15');
      });
    });
  });

  it('shows an unavailable score component', () => {
    wrapper = getMountedComponent({
      value: '.',
    });

    const scoreBackground = wrapper.find('[data-test=score-background]');
    expect(scoreBackground.attributes().style).to.contains('rosalution-grey-300');

    const scoreText = wrapper.find('[data-test=score-text]');
    expect(scoreText.attributes().style).to.contains('rosalution-grey-300');
  });
});
