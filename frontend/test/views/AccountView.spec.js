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
  let mockUser;
  let getUserStub;
  let generateSecretStub;
  let getAPICredentialsStub;

  beforeEach(() => {
    sandbox = sinon.createSandbox();
    mockUser = {
      clientSecret: 'testsecret',
    };

    getUserStub = sandbox.stub(authStore, 'getUser');
    getUserStub.returns(mockUser);

    generateSecretStub = sandbox.stub(authStore, 'generateSecret');
    getAPICredentialsStub = sandbox.stub(authStore, 'getAPICredentials');
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
    const wrapper = getMountedComponent();

    let credentialsBox = wrapper.findComponent('[data-test=credentials]');

    await credentialsBox.vm.$emit('display-secret');
    await wrapper.vm.$nextTick();

    credentialsBox = wrapper.findComponent('[data-test=credentials]');
    expect(credentialsBox.props('clientSecret')).to.equal(wrapper.vm.clientSecret);
  });

  it('should not toggle the secret value on click again after it has been toggled', async () => {
    const wrapper = getMountedComponent();

    let credentialsBox = wrapper.findComponent('[data-test=credentials]');

    await credentialsBox.vm.$emit('display-secret');
    await wrapper.vm.$nextTick();

    credentialsBox = wrapper.findComponent('[data-test=credentials]');
    expect(credentialsBox.props('clientSecret')).to.equal(wrapper.vm.clientSecret);
    await credentialsBox.vm.$emit('display-secret');
    await wrapper.vm.$nextTick();

    credentialsBox = wrapper.findComponent('[data-test=credentials]');
    expect(credentialsBox.props('clientSecret')).to.equal(wrapper.vm.clientSecret);
  });

  it('should use clientSecret prop in computed secretValue', async () => {
    const wrapper = getMountedComponent();

    let credentialsBox = wrapper.findComponent('[data-test=credentials]');
    expect(credentialsBox.props('clientSecret')).to.equal('<click to show>');

    getAPICredentialsStub.returns({client_secret: 'updatedSecret'});
    await credentialsBox.vm.$emit('generate-secret');
    await wrapper.vm.$nextTick();

    credentialsBox = wrapper.findComponent('[data-test=credentials]');
    expect(credentialsBox.props('clientSecret')).to.equal('<click to show>');

    await credentialsBox.vm.$emit('display-secret');
    await wrapper.vm.$nextTick();

    credentialsBox = wrapper.findComponent('[data-test=credentials]');
    expect(credentialsBox.props('clientSecret')).to.equal('updatedSecret');
  });

  it('should update clientSecret on multiple generate-secret calls', async () => {
    getAPICredentialsStub.onFirstCall().returns({client_secret: 'newSecret1'});
    getAPICredentialsStub.onSecondCall().returns({client_secret: 'newSecret2'});

    const wrapper = getMountedComponent();
    let credentialsBox = wrapper.findComponent('[data-test=credentials]');
    expect(credentialsBox.props('clientSecret')).to.equal('<click to show>');

    await credentialsBox.vm.$emit('generate-secret');
    await credentialsBox.vm.$emit('display-secret');
    await wrapper.vm.$nextTick();
    expect(generateSecretStub.calledOnce).to.be.true;
    credentialsBox = wrapper.findComponent('[data-test=credentials]');
    expect(credentialsBox.props('clientSecret')).to.equal('newSecret1');

    await credentialsBox.vm.$emit('generate-secret');
    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();
    expect(generateSecretStub.calledTwice).to.be.true;
    credentialsBox = wrapper.findComponent('[data-test=credentials]');
    expect(credentialsBox.props('clientSecret')).to.equal('newSecret2');
  });

  it('should initially hide the secret value in the CredentialsBox component', () => {
    const wrapper = getMountedComponent();
    const credentialsBox = wrapper.findComponent('[data-test=credentials]');
    expect(credentialsBox.props('clientSecret')).to.equal('<click to show>');
  });

  describe('when user.client_secret is not set', () => {
    let getUserEmptyStub;

    beforeEach(() => {
      sandbox.restore();
      sandbox = sinon.createSandbox();
      mockUser = {
        clientSecret: '',
      };

      getUserEmptyStub = sandbox.stub(authStore, 'getUser');
      getUserEmptyStub.returns(mockUser);
    });

    it('should return "<empty>" in the CredentialsBox component', () => {
      const wrapper = getMountedComponent();

      let credentialsBox = wrapper.findComponent('[data-test=credentials]');

      credentialsBox = wrapper.findComponent('[data-test=credentials]');
      expect(credentialsBox.props('clientSecret')).to.equal('<empty>');
    });
  });
});
