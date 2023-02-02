import {expect, describe, it, beforeAll, afterAll} from 'vitest';
import {config, shallowMount} from '@vue/test-utils';

import AnalysisListingHeader from '@/components/AnalysisListing/AnalysisListingHeader.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import {RouterLink} from 'vue-router';

/**
 * helper function that shadllow mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {
    username: '',
  };

  return shallowMount(AnalysisListingHeader, {
    props: {...defaultProps, ...props},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
        'router-link': RouterLink,
      },
    },
  });
}

beforeAll(() => {
  config.global.renderStubDefaultSlot = true;
});

afterAll(() => {
  config.global.renderStubDefaultSlot = false;
});

describe('AnalysisListingHeader.vue', () => {
  it('should provide no actions to display', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.attributes('actions')).to.be.empty;
  });

  it('should emit search event when search text has content', async () => {
    const wrapper = getMountedComponent();

    const searchTextInput = wrapper.get('[data-test="analysis-search"]');
    await searchTextInput.setValue('fake-search');

    const searchEvent = wrapper.emitted('update:searchText');
    expect(searchEvent).toHaveLength(1);
    expect(searchEvent[0]).toEqual(['fake-search']);
  });
});
