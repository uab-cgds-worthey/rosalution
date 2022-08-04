import {expect, describe, it, beforeAll, afterAll} from 'vitest';
import {config, shallowMount} from '@vue/test-utils';

import HeaderComponent from '@/components/HeaderComponent.vue';

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

  return shallowMount(HeaderComponent, {
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

describe('HeaderComponent.vue', () => {
  it('should display application title', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.html()).to.contains('rosalution');
  });

  it('should display "Login" in the upper right hand corner if username is a blank string', async () => {
    const wrapper = getMountedComponent();

    const userMenuWrapper = wrapper.find('[data-test=user-menu]');

    expect(userMenuWrapper.text()).to.contain('LOGIN');
  });

  it('should properly display the username in the upper right hand corner', async () => {
    const wrapper = getMountedComponent({
      username: 'UABProvider',
    });
    const userMenuWrapper = wrapper.find('[data-test=user-text]');

    expect(userMenuWrapper.text()).to.contain('UABProvider');
  });
});
