import {expect, afterEach, beforeEach, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';
import sinon from 'sinon';

import AccountView from '@/views/AccountView.vue';

import {authStore} from '@/stores/authStore.js';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import {RouterLink} from 'vue-router';

/**
 * Helper that mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {
    username: authStore.getUser().username,
  };


  return shallowMount(AccountView, {
    props: {...defaultProps, ...props},
    attachTo: document.body,
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
        'router-link': RouterLink,
      },
      mocks: {
        $route: {
          push: sinon.spy(),
        },
        $router: {
          push: sinon.spy(),
        },
      },
    },
  });
}

describe('AccountView.vue', () => {
  const sandbox = sinon.createSandbox();
  let wrapper;
  const mockAuthStore = {
    getUser: (options = {}) => {
      const defaultUser = {
        username: 'testuser',
        full_name: 'Test User',
        email: 'testuser@example.com',
        clientId: 'testclientid',
      };
      
      if (options.clientSecret) {
        return {...defaultUser, clientSecret: options.clientSecret};
      } else {
        return {...defaultUser, clientSecret: ''};
      }
    },
  };

  beforeEach(() => {
    wrapper = getMountedComponent();
  });

  afterEach(() => {
    sandbox.restore();
  });

  it('contains the expected content body element', () => {
    const appHeader = wrapper.find('app-header');
    expect(appHeader.exists()).to.be.true;

    const appContent = wrapper.find('app-content');
    expect(appContent.exists()).to.be.true;
  });

  it('should have a secretValue computed property', () => {
  const secretValue = wrapper.vm.secretValue;
  expect(secretValue).to.exist;
  });

  describe('the header', () => {
    it('contains a header element', () => {
      const appHeader = wrapper.find('app-header');
      expect(appHeader.exists()).to.be.true;
    });

    it('should logout on the header logout event', async () => {
      const headerComponent = wrapper.getComponent(
          '[data-test=rosalution-header]',
      );
      headerComponent.vm.$emit('logout');
      await headerComponent.vm.$nextTick();

      expect(wrapper.vm.$router.push.called).to.be.true;
    });
  });

    // Test case where clientSecret is set
  it('should return ["<click to show>"] when user.clientSecret is set', () => {
    const user = mockAuthStore.getUser({clientSecret: 's26zcWlArYQJVW3eaL2Rl8awimSk0Us3'});
    sandbox.stub(authStore, 'getUser').returns(user);
    console.log(user);

    const secretValue = wrapper.vm.secretValue;
    console.log(secretValue)
    expect(secretValue).to.deep.equal(['<click to show>']);
  });

  // Test case where clientSecret is not set
  it('should return ["<empty>"] when user.clientSecret is not set', () => {
    const user = mockAuthStore.getUser();
    sandbox.stub(authStore, 'getUser').returns(user);
    console.log(user)

    const secretValue = wrapper.vm.secretValue;
    expect(secretValue).to.deep.equal(['<empty>']);
  });
});
