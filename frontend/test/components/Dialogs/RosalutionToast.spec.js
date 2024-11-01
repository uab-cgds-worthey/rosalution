import {it, expect, describe, beforeEach, beforeAll, afterEach} from 'vitest';
import {shallowMount} from '@vue/test-utils';
import sinon from 'sinon';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

import RosalutionToast from '@/components/Dialogs/RosalutionToast.vue';

describe('Toast.vue', () => {
  let wrapper;
  let sandbox;
  let toast;

  beforeAll(() => {
    sandbox = sinon.createSandbox();
  });

  beforeEach(() => {
    wrapper = shallowMount(RosalutionToast, {
      global: {
        components: {
          'font-awesome-icon': FontAwesomeIcon,
        },
        stubs: {
          transition: false,
        },
      },
    });
    toast = wrapper.vm;
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
    const toastContainer = wrapper.find('[data-test=toast-container]');
    expect(toastContainer.exists()).to.be.true;

    const closeIconElement = wrapper.get('[data-test=toast-close-button]');
    await closeIconElement.trigger('click');

    const closedContainer = wrapper.find('[data-test=toast-container]');
    expect(closedContainer.exists()).to.be.false;
  });

  it('displays different and multiple prompts to the toast', async () => {
    toast.info('hello world first time');
    await wrapper.vm.$nextTick();

    expect(wrapper.html()).to.include('hello world first time');

    toast.error('hello world error');
    await wrapper.vm.$nextTick();
    expect(wrapper.html()).to.include('hello world error');

    toast.cancel();
    await wrapper.vm.$nextTick();
  });
});

