import {describe, it, beforeEach, expect} from 'vitest';
import {shallowMount} from '@vue/test-utils';
import sinon from 'sinon';

import SupplementalFormList from '../../../src/components/AnalysisView/SupplementalFormList.vue';
import ModalDialog from '../../../src/components/AnalysisView/ModalDialog.vue';

describe('SupplementalFormList.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(SupplementalFormList);
  });

  it('Vue instance exists and it is an object', () => {
    expect(typeof wrapper).toBe('object');
  });

  it('plus-logo pops up the add attachment modal', async () => {
    const button = wrapper.find('[data-test=add-button]');

    await button.trigger('click');

    const modal = wrapper.find('[data-test=modal-dialog]');

    expect(modal.exists()).to.equal(true);
  });

  it('new file populates in a row', async () => {
    const onModalDialogSpy = sinon.spy(wrapper.vm, 'showAttachDocumentModal');
    const onAttachmentSpy = sinon.spy(wrapper.vm, 'onAttachmentChange');

    await wrapper.setData({showModal: true});

    const modalWrapper = wrapper.findComponent(ModalDialog);

    modalWrapper.vm.$emit('addattachment', {
      data: 'fakeFiledData',
      name: '/path/to/fakeFile.ext',
      type: 'file',
    });

    modalWrapper.vm.$emit('closemodal');

    expect(wrapper.findAll('tr').length).toBe(1);

    await wrapper.vm.$nextTick();

    expect(onModalDialogSpy.called).toBe(true);
    expect(onAttachmentSpy.called).toBe(true);
    expect(wrapper.findAll('tr').length).toBe(2);
    expect(wrapper.vm.$data.attachments.length).toBe(1);
  });

  // These have not been implemented yet with the new design.
  it.skip('clicking comment-logo pops up the comment modal', () => {});
  it.skip('clicking edit-logo pops up the edit modal', () => {});
  // This test will be added when the Modal dialog is completed to attch links and files.
  it.skip('correct logo displays based on attachment type', () => {});
});