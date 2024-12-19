import {describe, it, beforeEach, expect} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import InputDialogExistingAttachments from '@/components/Dialogs/InputDialogExistingAttachments.vue';

describe('InputDialogExistingAttachments.vue', () => {
  let wrapper;

  beforeEach(() => {
    const defaultProps = {
      userInput: {
        'name': '',
        'data': '',
        'comments': '',
      },
    };
    wrapper = shallowMount(InputDialogExistingAttachments, {
      props: {
        ...defaultProps,
      },
    });
  });

  it('is showing the existing attachments', async () => {
    expect(wrapper.exists()).to.be.true;
  });
});
