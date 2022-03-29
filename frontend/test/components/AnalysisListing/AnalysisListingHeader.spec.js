import {expect, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import AnalysisListingHeader from '@/components/AnalysisListing/AnalysisListingHeader.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

/**
 * helper function that shadllow mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {
  };

  return shallowMount(AnalysisListingHeader, {
    props: {...defaultProps, ...props},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
      },
    },
  });
}

describe('AnalysisListingHeader.vue', () => {
  it('should display application title', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.html()).to.contains('diverGen');
  });

  it('should emit search event when search text has content', async () => {
    const wrapper = getMountedComponent();
    const searchTextInput = wrapper.get('[data-test="analysis-search"]');
    await searchTextInput.setValue('fake-search');

    const searchEvent = wrapper.emitted('search');
    expect(searchEvent).toHaveLength(1);
    expect(searchEvent[0]).toEqual(['fake-search']);
  });
});
