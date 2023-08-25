import {expect, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import AnalysisListingLegend from '@/components/AnalysisListing/AnalysisListingLegend.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

/**
 * helper function that shallow mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {};

  return shallowMount(AnalysisListingLegend, {
    props: {...defaultProps, ...props},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
      },
    },
  });
}

describe('AnalysisListingLegend.vue', () => {
  it('should display several states of rosalution analyses', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.html()).to.contains('Ready');
    expect(wrapper.html()).to.contains('Active');
  });

  it('should all be colored when no statuses are being filtered for', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.html()).to.not.contains('color: var(--rosalution-grey-300)');
  });

  it('should only color the filtered status', async () => {
    const wrapper = getMountedComponent();
    const readyDomElement = wrapper.find('[data-test="Ready"]');

    await readyDomElement.trigger('click');

    const statusDomElements = wrapper.findAll('.status');
    statusDomElements.forEach( (statusElement) => {
      if (statusElement.text() === 'Ready') {
        expect(readyDomElement.html()).to.contains('color: var(--rosalution-status-ready)');
      } else {
        expect(wrapper.html()).to.contains(`color: var(--rosalution-grey-300)`);
      }
    });
  });

  it('should emit a filtered-changed event when a status is clicked', async () => {
    const wrapper = getMountedComponent();
    const readyDomElement = wrapper.find('[data-test="Ready"]');

    await readyDomElement.trigger('click');
    expect(wrapper.emitted()).to.have.property('filtered-changed');
    expect(wrapper.emitted()['filtered-changed'][0][0]).to.contains('Ready');
  });
});
