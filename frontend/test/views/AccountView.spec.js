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
  return shallowMount(AccountView, {
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
  let sandbox;

  beforeEach(() => {
    sandbox = sinon.createSandbox();
  });

  afterEach(() => {
    sandbox.restore();
  });

  it('contains the expected content body element', () => {
    const wrapper = getMountedComponent();
    const appHeader = wrapper.find('app-header');
    expect(appHeader.exists()).to.be.true;

    const appContent = wrapper.find('app-content');
    expect(appContent.exists()).to.be.true;
  });

  it('should have a secretValue computed property', () => {
    const wrapper = getMountedComponent();
    const secretValue = wrapper.vm.secretValue;
    expect(secretValue).to.exist;
  });

  describe('the header', () => {
    it('contains a header element', () => {
      const wrapper = getMountedComponent();
      const appHeader = wrapper.find('app-header');
      expect(appHeader.exists()).to.be.true;
    });

    it('should logout on the header logout event', async () => {
      const wrapper = getMountedComponent();
      const headerComponent = wrapper.getComponent(
          '[data-test=rosalution-header]',
      );
      headerComponent.vm.$emit('logout');
      await headerComponent.vm.$nextTick();

      expect(wrapper.vm.$router.push.called).to.be.true;
    });
  });

  it('should toggle the secret value on click', async () => {
    // Create a stub for the getUser method and return a mock user
    const mockUser = {
      clientSecret: 'testsecret',
    };

    const getUserStub = sandbox.stub(authStore, 'getUser');
    getUserStub.returns(mockUser);

    const wrapper = getMountedComponent();

    expect(wrapper.vm.showSecretValue).to.be.false;
    expect(wrapper.vm.secretValue).to.deep.equal(['<click to show>']);

    // Find the section box component for the "Client Secret" section
    const sectionBox = wrapper.findComponent({ref: 'credentials'});

    // Simulate a click event on the section box
    await sectionBox.trigger('click');

    // Assert that showSecretValue has been toggled
    expect(wrapper.vm.showSecretValue).to.be.true;

    // Assert that the computed secretValue property returns the client secret
    expect(wrapper.vm.secretValue).to.deep.equal([wrapper.vm.user.clientSecret]);

    // Simulate a second click event on the section box
    await sectionBox.trigger('click');

    // Assert that showSecretValue remains true after the second click
    expect(wrapper.vm.showSecretValue).to.be.true;

    // Assert that the computed secretValue property remains the client secret
    expect(wrapper.vm.secretValue).to.deep.equal([wrapper.vm.user.clientSecret]);
  });

  // Test case where clientSecret is not set
  it('should return ["<empty>"] when user.client_secret is not set', () => {
    // Create a stub for the getUser method and return a mock user
    const mockUser = {
      clientSecret: '',
    };

    const getUserStub = sandbox.stub(authStore, 'getUser');
    getUserStub.returns(mockUser);

    const wrapper = getMountedComponent();

    expect(wrapper.vm.secretValue).to.deep.equal(['<empty>']);
  });
});
