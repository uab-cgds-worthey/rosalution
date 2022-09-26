import {it, expect, describe, beforeEach} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import RemoveFileConfirmationDialog from '@/components/AnalysisView/RemoveFileConfirmationDialog.vue';

describe('RemoveFileConfirmationDialog.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(RemoveFileConfirmationDialog, {});
  });

  it('Vue instance exists and it is an object', () => {
    expect(typeof wrapper).toBe('object');
  });

  it('Should emit "deleteattachment" after clicking on the Delete button', async () => {
    wrapper.find('[data-test=delete-item-button]').trigger('click');
    expect(wrapper.emitted().delete).to.not.be.undefined;
  });

  it('Should emit "cancelconfirmation" after clicking on the Cancel button', async () => {
    wrapper.find('[data-test=cancel-modal-button]').trigger('click');
    expect(wrapper.emitted().cancel).to.not.be.undefined;
  });
});

