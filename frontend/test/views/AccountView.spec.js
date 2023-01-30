import {expect, afterEach, beforeEach, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import sinon from 'sinon';

import AccountView from '@/views/AccountView.vue';

import {authStore} from '@/stores/authStore.js';

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
  let mockGetUser;

  beforeEach(() => {
  mockGetUser = sandbox.stub(authStore, 'getUser').returns({username: 'test'});
  });

  afterEach(() => {
    sandbox.restore();
  });

  it('displays the username correctly', () => {
  const wrapper = getMountedComponent();
  const pTag = wrapper.find('p');

  expect(pTag.text()).to.include('test');
  })
})