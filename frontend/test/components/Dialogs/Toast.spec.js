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

  it('should render the info title for info type messages', async () => {
    toast.info();
    await wrapper.vm.$nextTick();

    const titleElement = wrapper.get('[data-test=toast-title-type]');
    expect(titleElement.text()).to.equal('Info');
  });

  it('should render the success title for success type messages', async () => {
    toast.success();
    await wrapper.vm.$nextTick();

    const titleElement = wrapper.get('[data-test=toast-title-type]');
    expect(titleElement.text()).to.equal('Success');
  });

  it('should render the error title for error type messages', async () => {
    toast.error();
    await wrapper.vm.$nextTick();

    const titleElement = wrapper.get('[data-test=toast-title-type]');
    expect(titleElement.text()).to.equal('Error');
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

