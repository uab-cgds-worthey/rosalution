import {expect, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';
import UserInfoBox from '@/components/AccountView/UserInfoBox.vue';

/**
 * Helper function that shallow mounts and returns the rendered component
 * @param {Object} props Props for testing to overwrite default props
 * @return {VueWrapper} Returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {
    header: '',
    username: '',
    fullName: '',
    email: '',
  };

  return shallowMount(UserInfoBox, {
    propsData: {...defaultProps, ...props},
  });
}

describe('UserInfoBox.vue', () => {
  it('renders the correct username', () => {
    const username = 'johndoe';
    const wrapper = getMountedComponent({username});

    expect(wrapper.find('[data-test="username"]').text()).to.equal('johndoe');
  });

  it('renders the correct full name', () => {
    const fullName = 'John Doe';
    const wrapper = getMountedComponent({fullName});

    expect(wrapper.find('[data-test="full-name"]').text()).to.equal('John Doe');
  });

  it('renders the correct email', () => {
    const email = 'john.doe@example.com';
    const wrapper = getMountedComponent({email});

    expect(wrapper.find('[data-test="email"]').text()).to.equal('john.doe@example.com');
  });
});
