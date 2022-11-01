import {afterEach, beforeEach, describe, it, expect} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import sinon from 'sinon';

import LogoutView from '@/views/LogoutView.vue';

import {authStore} from '@/stores/authStore.js';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

/**
 * Helper that mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  return shallowMount(LogoutView, {
    props: {...props},
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

describe('LogoutView.vue', () => {
  const sandbox = sinon.createSandbox();

  let mockedLogout;
  let mockedGetToken;

  beforeEach(() => {
    mockedLogout = sandbox.stub(authStore, 'logout');
    mockedGetToken = sandbox.stub(authStore, 'getToken');
  });

  afterEach(() => {
    sandbox.restore();
  });

  it('If a token exists in the authStore, re-route the user to specified page', async () => {
    const spy = sinon.spy(LogoutView.methods, 'redirectUrl');

    mockedGetToken.returns('returns');
    mockedLogout.returns({url: 'www.fakewebsite.com'});

    const wrapper = getMountedComponent();

    await wrapper.vm.$nextTick();

    expect(spy.calledWith('www.fakewebsite.com')).to.equal(true);
  });
});
