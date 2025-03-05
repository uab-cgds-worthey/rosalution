import {describe, it, beforeEach, expect} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import InputDialogExistingAttachments from '@/components/Dialogs/InputDialogExistingAttachments.vue';

describe('InputDialogExistingAttachments.vue', () => {
  let wrapper;

  beforeEach(() => {
    const defaultProps = {
      existingAttachments: [
        {
          'name': 'google',
          'data': 'www.google.com',
          'attachment_id': 'f45a7f81-53dc-4e77-9826-e45b779637a6',
          'type': 'link',
          'comments': 'test link attachment',
        },
        {
          'name': 'Screenshot 2024-12-12 at 2.05.56 PM.png',
          'attachment_id': '6765a3d392c28d5021f6f7be',
          'type': 'file',
          'comments': 'James graduating',
        },
      ],
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

  it('is displaying list of existing evidences', async () => {
    const evidenceList = wrapper.find('[data-test=existing-attachments-list]');
    expect(evidenceList.exists()).to.be.true;
  });
});
