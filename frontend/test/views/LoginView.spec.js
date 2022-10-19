import {expect, afterEach, beforeEach, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import sinon from 'sinon';

import LoginView from '@/views/LoginView.vue';

import {authStore} from '@/stores/authStore.js';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

/**
 * Helper that mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {
    username: '',
  };

  return shallowMount(LoginView, {
    props: {...defaultProps, ...props},
    attachTo: document.body,
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
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

describe('LoginView.vue', () => {
  const sandbox = sinon.createSandbox();
  let mockLoginDevelopment;
  let mockLoginUAB;

  beforeEach(() => {
    mockLoginDevelopment = sandbox.stub(authStore, 'loginDevelopment');
    mockLoginUAB = sandbox.stub(authStore, 'loginUAB');
  });

  afterEach(() => {
    sandbox.restore();
  });

  it('When login button pressed, does it call the Development Login with the correct parameters', async () => {
    const wrapper = getMountedComponent();

    const userInput = wrapper.find('[data-test=username-input]');
    const localLoginButton = wrapper.find('[data-test=local-login-button]');

    await userInput.setValue('UABProvider');
    await wrapper.vm.$nextTick();

    localLoginButton.trigger('click');
    await wrapper.vm.$nextTick();

    expect(mockLoginDevelopment.calledWith(fakeUserData)).toBe(true);
  });

  it('When the UAB login button is pressed, does it call the UAB Login function', async () => {
    const wrapper = getMountedComponent();

    const prodLoginButton = wrapper.find('[data-test=prod-login-button]');

    prodLoginButton.trigger('click');
    await wrapper.vm.$nextTick();

    expect(mockLoginUAB.called).toBe(true);
  });
});

const fakeUserData = {'username': 'UABProvider', 'password': ''};
