import {expect, afterEach, beforeEach, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import Auth from '@/models/authentication.js';
import sinon from 'sinon';

import LoginView from '@/views/LoginView.vue';

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
  let mockOAuthLogin;
  let mockUABCASLogin;

  beforeEach(() => {
    mockOAuthLogin = sandbox.stub(Auth, 'loginOAuth');
    mockUABCASLogin = sandbox.stub(Auth, 'loginCas');
  });

  afterEach(() => {
    sandbox.restore();
  });

  it('When login button pressed, does it call the oauth2 function with the correct parameters', async () => {
    const wrapper = getMountedComponent();

    const userInput = wrapper.find('[data-test=username-input]');
    const localLoginButton = wrapper.find('[data-test=local-login-button]');

    await userInput.setValue('UABProvider');
    await wrapper.vm.$nextTick();

    localLoginButton.trigger('click');
    await wrapper.vm.$nextTick();

    expect(mockOAuthLogin.calledWith(fakeUserData)).toBe(true);
  });

  it('When the UAB login button is pressed, does it call the CAS login function', async () => {
    const wrapper = getMountedComponent();

    const prodLoginButton = wrapper.find('[data-test=prod-login-button]');

    prodLoginButton.trigger('click');
    await wrapper.vm.$nextTick();

    expect(mockUABCASLogin.called).toBe(true);
  });
});

const fakeUserData = {'username': 'UABProvider', 'password': 'secret'};
