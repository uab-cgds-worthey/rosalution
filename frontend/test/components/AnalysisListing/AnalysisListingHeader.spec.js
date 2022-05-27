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
  config.renderStubDefaultSlot = true;
});

afterAll(() => {
  config.renderStubDefaultSlot = false;
});

describe('AnalysisListingHeader.vue', () => {
  it('should display application title', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.html()).to.contains('diverGen');
  });

  it('should display "Login" in the upper right hand corner if username is a blank string', async () => {
    const wrapper = getMountedComponent();

    const userMenuWrapper = wrapper.find('[data-test=user-menu]');

    expect(userMenuWrapper.text()).to.contain('LOGIN');
  });

  it('should emit search event when search text has content', async () => {
    const wrapper = getMountedComponent();

    const searchTextInput = wrapper.get('[data-test="analysis-search"]');
    await searchTextInput.setValue('fake-search');

    const searchEvent = wrapper.emitted('search');
    expect(searchEvent).toHaveLength(1);
    expect(searchEvent[0]).toEqual(['fake-search']);
  });

  it('should properly display the username in the upper right hand corner', async () => {
    const wrapper = getMountedComponent({
      username: 'UABProvider',
    });
    const userMenuWrapper = wrapper.find('[data-test=user-text]');

    expect(userMenuWrapper.text()).to.contain('UABProvider');
  });
});
