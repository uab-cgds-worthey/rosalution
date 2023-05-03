import {it, expect, describe, beforeEach, beforeAll, afterEach} from 'vitest';
import {shallowMount} from '@vue/test-utils';
import sinon from 'sinon';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

import Toast from '@/components/Dialogs/Toast.vue';
import toast from '@/toast.js';

describe('Dialog.vue', () => {
  let wrapper;
  let sandbox;

  beforeAll(() => {
    sandbox = sinon.createSandbox();
  });

  beforeEach(() => {
    wrapper = shallowMount(Toast, {
      global: {
        components: {
          'font-awesome-icon': FontAwesomeIcon,
        },
      },
    });
  });

  afterEach(() => {
    sandbox.resetHistory();
  });

  it('should render the type as a message title', async () => {
    [
      // {
      //   expected_state: 'Info',
      //   method: toast.info,
      // },
      {
        expected_state: 'Success',
        method: toast.success,
      },
      {
        expected_state: 'Error',
        method: toast.error,
      },
    ].forEach(async (test) => {
      test.method();
      await wrapper.vm.$nextTick();

      const titleElement = wrapper.get('[data-test=toast-title-type]');
      expect(titleElement.text()).to.equal(test.expected_state);

      const closeIconElement = wrapper.get('[data-test=toast-close-button]');
      closeIconElement.trigger('click');
      await wrapper.vm.$nextTick();
    });
  });

  it('should render a toast message', async () => {
    toast.info('hello world');
    await wrapper.vm.$nextTick();

    expect(wrapper.html()).to.include('hello world');
  });

  it('should allow the user to close', async () => {
    toast.info('hello world');
    await wrapper.vm.$nextTick();

    const closeIconElement = wrapper.get('[data-test=toast-close-button]');
    closeIconElement.trigger('click');
    await wrapper.vm.$nextTick();

    const toastContainer = wrapper.find('[data-test=toast-container]');
    expect(toastContainer.exists()).to.be.false;
  });
});

