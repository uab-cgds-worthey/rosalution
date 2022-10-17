import {describe, it, beforeEach, expect} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import InputDialogAttachUrl from '@/components/Dialogs/InputDialogAttachUrl.vue';

describe('InputDialogAttachUrl.vue', () => {
  let wrapper;

  beforeEach(() => {
    const defaultProps = {
      userInput: {
        'name': '',
        'data': '',
        'comments': '',
      },
    };
    wrapper = shallowMount(InputDialogAttachUrl, {
      props: {
        ...defaultProps,
      },
    });
  });

  it('should update user input when a link name is filled', async () => {
    const actualLinkName = 'it-is-a-link-name';

    const input = wrapper.find('[data-test=name-input]');
    input.setValue(actualLinkName);

    await input.trigger('change');

    expect(wrapper.emitted()['update:userInput']).to.not.be.undefined;
    expect(wrapper.emitted()['update:userInput'][0][0].name).to.equal('it-is-a-link-name');
  });

  it('should update user input when a link is filled', async () => {
    const actualLink = 'it-is-a-link';

    const input = wrapper.find('[data-test=link-input]');
    input.setValue(actualLink);

    await input.trigger('change');

    expect(wrapper.emitted()['update:userInput']).to.not.be.undefined;
    expect(wrapper.emitted()['update:userInput'][0][0].data).to.equal('it-is-a-link');
  });

  it('should update user input when comments are filled', async () => {
    const actualComments = 'it-is-a-comment';

    const input = wrapper.find('[data-test=comments-text-area]');
    input.setValue(actualComments);

    await input.trigger('change');

    expect(wrapper.emitted()['update:userInput']).to.not.be.undefined;
    expect(wrapper.emitted()['update:userInput'][0][0].comments).to.equal('it-is-a-comment');
  });
});
