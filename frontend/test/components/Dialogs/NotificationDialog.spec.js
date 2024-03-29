import {it, expect, describe, beforeEach, beforeAll, afterEach} from 'vitest';
import {shallowMount} from '@vue/test-utils';
import sinon from 'sinon';

import NotificationDialog from '@/components/Dialogs/NotificationDialog.vue';
import notificationDialog from '@/notificationDialog.js';

describe('Dialog.vue', () => {
  let wrapper;
  let sandbox;

  beforeAll(() => {
    sandbox = sinon.createSandbox();
  });

  beforeEach(() => {
    wrapper = shallowMount(NotificationDialog);
  });

  afterEach(() => {
    sandbox.resetHistory();
  });

  it('should render the title', async () => {
    notificationDialog
        .title('heya!')
        .alert('hello world');
    await wrapper.vm.$nextTick();

    const titleElement = wrapper.get('h2');
    expect(titleElement.text()).to.include('heya!');
  });

  describe('the alert', async () => {
    it('should display alert message', async () => {
      notificationDialog.alert('hello world');
      await wrapper.vm.$nextTick();

      expect(wrapper.html()).to.include('hello world');
    });

    it('should render ok button', async () => {
      notificationDialog.alert('hello world');
      await wrapper.vm.$nextTick();
      const okButton = wrapper.get('[data-test=confirm-button]');
      expect(okButton.text()).to.equal('Ok');
    });
  });

  describe(('the notification'), () => {
    it('can be canceled', async () => {
      notificationDialog.confirm('are you really sure?').then((confirmed) => {
        expect(confirmed).to.be.false;
      });
      await wrapper.vm.$nextTick();

      const cancelButton = wrapper.get('[data-test=cancel-button]');
      expect(cancelButton.text()).to.equal('Cancel');
      cancelButton.trigger('click');
    });

    it('can be confirmed', async () => {
      notificationDialog.confirm('are you sure for real for real?').then((confirmed) => {
        expect(confirmed).to.be.true;
      });
      await wrapper.vm.$nextTick();

      const confirmButton = wrapper.get('[data-test=confirm-button]');
      expect(confirmButton.text()).to.equal('Ok');
      confirmButton.trigger('click');
    });
  });
});

