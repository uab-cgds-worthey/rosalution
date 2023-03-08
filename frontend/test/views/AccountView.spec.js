import {expect, afterEach, beforeEach, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';
import sinon from 'sinon';

import AccountView from '@/views/AccountView.vue';

import {authStore} from '@/stores/authStore.js';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import {RouterLink} from 'vue-router';
import { nextTick } from 'vue';

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

  beforeEach(() => {
    sandbox = sinon.createSandbox();
    mockUser = {
    clientSecret: 'testsecret',
    };

    getUserStub = sandbox.stub(authStore, 'getUser');
    getUserStub.returns(mockUser);
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
    const wrapper = getMountedComponent();

    let sectionBox = wrapper.findComponent('[data-test=credentials]');
  
    await sectionBox.trigger('click');
    await wrapper.vm.$nextTick();

    sectionBox = wrapper.findComponent('[data-test=credentials]');
    expect(sectionBox.props('content')[1].value).toEqual([wrapper.vm.user.clientSecret]);
  });

  it('should not toggle the secret value on click again after it has been toggled', async () => {
    const wrapper = getMountedComponent();

    let sectionBox = wrapper.findComponent('[data-test=credentials]');

    await sectionBox.trigger('click');
    await wrapper.vm.$nextTick();

    sectionBox = wrapper.findComponent('[data-test=credentials]');
    expect(sectionBox.props('content')[1].value).toEqual([wrapper.vm.user.clientSecret]);
    await sectionBox.trigger('click');
    await wrapper.vm.$nextTick();

    sectionBox = wrapper.findComponent('[data-test=credentials]');
    expect(sectionBox.props('content')[1].value).toEqual([wrapper.vm.user.clientSecret]);
  });

  // Test case where clientSecret is not set
  it('should return ["<empty>"] when user.client_secret is not set', () => {
    sandbox.restore();
    sandbox = sinon.createSandbox();
    mockUser = {
      clientSecret: '',
    };

    const getUserEmptyStub = sandbox.stub(authStore, 'getUser');
    getUserEmptyStub.returns(mockUser);

    const wrapper = getMountedComponent();

    expect(wrapper.vm.secretValue).toEqual(['<empty>']);
  });
});
