import {expect, describe, it} from 'vitest';
import {config, shallowMount} from '@vue/test-utils';

import LoginView from '@/views/LoginView.vue';

/**
 * helper function that shadllow mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {
    username: '',
  };

  return shallowMount(LoginView, {
    props: {...defaultProps, ...props},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
        'router-link': RouterLink,
      },
    },
  });
}

describe('LoginView.vue', () => {
  it('should just pass', () => {
    const wrapper = getMountedComponent();
    expect(1).to.equal(1)
  })
});
