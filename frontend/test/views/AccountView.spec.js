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
    expect(credentialsBox.props('clientSecret')).toEqual(wrapper.vm.clientSecret);
  });

  it('should not toggle the secret value on click again after it has been toggled', async () => {
    const wrapper = getMountedComponent();

    let credentialsBox = wrapper.findComponent('[data-test=credentials]');

    await credentialsBox.vm.$emit('display-secret');
    await wrapper.vm.$nextTick();

    credentialsBox = wrapper.findComponent('[data-test=credentials]');
    expect(credentialsBox.props('clientSecret')).toEqual(wrapper.vm.clientSecret);
    await credentialsBox.vm.$emit('display-secret');
    await wrapper.vm.$nextTick();

    credentialsBox = wrapper.findComponent('[data-test=credentials]');
    expect(credentialsBox.props('clientSecret')).toEqual(wrapper.vm.clientSecret);
  });


  it('should return "<empty>" when user.client_secret is not set', () => {
    sandbox.restore();
    sandbox = sinon.createSandbox();
    mockUser = {
      clientSecret: '',
    };

    const getUserEmptyStub = sandbox.stub(authStore, 'getUser');
    getUserEmptyStub.returns(mockUser);

    const wrapper = getMountedComponent();

    let credentialsBox = wrapper.findComponent('[data-test=credentials]');

    credentialsBox = wrapper.findComponent('[data-test=credentials]');
    expect(credentialsBox.props('clientSecret')).toEqual('<empty>');
  });

  it('should call onGenerateSecret method and update clientSecret', async () => {
    getAPICredentialsStub.returns({ client_secret: 'newSecret' });

    const wrapper = getMountedComponent();
    let credentialsBox = wrapper.findComponent('[data-test=credentials]');

    await credentialsBox.vm.$emit('generateSecret');
    await wrapper.vm.$nextTick();

    expect(generateSecretStub.called).to.be.true;
    expect(getAPICredentialsStub.called).to.be.true;
    expect(wrapper.vm.clientSecret).to.equal('newSecret');
  });

  it('should update showSecretValue to true when updateSecretValue is called', () => {
    const wrapper = getMountedComponent();
    wrapper.vm.updateSecretValue();
    expect(wrapper.vm.showSecretValue).to.be.true;
  });

  it('should update clientSecret on multiple generateSecret calls', async () => {
    getAPICredentialsStub.onFirstCall().returns({ client_secret: 'newSecret1' });
    getAPICredentialsStub.onSecondCall().returns({ client_secret: 'newSecret2' });

    const wrapper = getMountedComponent();
    let credentialsBox = wrapper.findComponent('[data-test=credentials]');

    await credentialsBox.vm.$emit('generateSecret');
    await wrapper.vm.$nextTick();
    expect(generateSecretStub.calledOnce).to.be.true;
    expect(getAPICredentialsStub.calledOnce).to.be.true;
    expect(wrapper.vm.clientSecret).to.equal('newSecret1');

    await credentialsBox.vm.$emit('generateSecret');
    await wrapper.vm.$nextTick();
    expect(generateSecretStub.calledTwice).to.be.true;
    expect(getAPICredentialsStub.calledTwice).to.be.true;
    expect(wrapper.vm.clientSecret).to.equal('newSecret2');
  });

  it('should return clientSecret when showSecretValue is true', () => {
    const wrapper = getMountedComponent();
    wrapper.vm.showSecretValue = true;
    expect(wrapper.vm.secretValue).to.equal(wrapper.vm.clientSecret);
  });

  it('should return "<click to show>" when showSecretValue is false and clientSecret is not empty', () => {
    const wrapper = getMountedComponent();
    wrapper.vm.showSecretValue = false;
    expect(wrapper.vm.secretValue).to.equal('<click to show>');
  });
});
