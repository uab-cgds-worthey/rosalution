import {expect, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import AnalysisListingLegend from '@/components/AnalysisListing/AnalysisListingLegend.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

/**
 * helper function that shadllow mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {
  };

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
});
