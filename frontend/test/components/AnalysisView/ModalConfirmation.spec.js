import {it, expect, describe, beforeEach} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import ModalConfirmation from '@/components/AnalysisView/ModalConfirmation.vue';

describe('ModalConfirmation.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(ModalConfirmation, {});
  });

  it('Vue instance exists and it is an object', () => {
    expect(typeof wrapper).toBe('object');
  });

  it('Should emit "deleteattachment" after clicking on the Delete button', async () => {
    wrapper.find('[data-test=delete-item-button]').trigger('click');
    expect(wrapper.emitted().deleteattachment).to.not.be.undefined;
  });

  it('Should emit "cancelconfirmation" after clicking on the Cancel button', async () => {
    wrapper.find('[data-test=cancel-modal-button]').trigger('click');
    expect(wrapper.emitted().cancelconfirmation).to.not.be.undefined;
  });

  it('Should emit "cancelconfirmation" after clicking on the Delete button', async () => {
    wrapper.find('[data-test=delete-item-button]').trigger('click');
    expect(wrapper.emitted().cancelconfirmation).to.not.be.undefined;
  });
});

