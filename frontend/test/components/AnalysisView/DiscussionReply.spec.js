import {it, expect, describe} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import ContextMenu from '../../../src/components/ContextMenu.vue';
import DiscussionReply from '../../../src/components/AnalysisView/DiscussionReply.vue';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

/**
 * Helper mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {
    replyId: '6905754b-554e-44f7-9553-8d622710e303',
    authorId: 'fake-user-id',
    authorName: 'Developer Person',
    publishTimestamp: '2024-10-09T21:13:22.687000',
    content: 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
    actions: [{text: 'Edit'}, {text: 'Delete'}],
  };

  return shallowMount(DiscussionReply, {
    props: {...defaultProps, ...props},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
      },
    },
  });
}

describe('DiscussionReply.vue', () => {
  it('Vue instance exists and it is an object', () => {
    const wrapper = getMountedComponent();
    expect(typeof wrapper).to.not.be.undefined;
  });

  it('Should display a context menu for a user that authored a discussion reply', () => {
    const wrapper = getMountedComponent({userClientId: 'fake-user-id'});

    const contextMenu = wrapper.find('[data-test=discussion-reply-context-menu]');

    expect(contextMenu.exists()).toBe(true);
  });

  it('Should not display a context menu for a user that did not author the discussion reply', () => {
    const wrapper = getMountedComponent({userClientId: 'different-fake-user-id'});

    const contextMenu = wrapper.find('[data-test=discussion-reply-context-menu]');

    expect(contextMenu.exists()).toBe(false);
  });

  it('Should recieve an emit to delete a reply and emits a reply:delete with replyId', async () => {
    const wrapper = getMountedComponent({userClientId: 'fake-user-id'});

    const replyId = '6905754b-554e-44f7-9553-8d622710e303';

    const contextMenu = wrapper.getComponent(ContextMenu);

    contextMenu.vm.$emit('delete', replyId);

    await wrapper.vm.$nextTick();

    const emittedObject = wrapper.emitted()['reply:delete'][0];

    expect(emittedObject[0]).toBe(replyId);
  });

  it('Should recieve an emit to edit a reply and emits reply:edit with new reply content on confirmation', async () => {
    const wrapper = getMountedComponent({userClientId: 'fake-user-id'});

    const contextMenu = wrapper.getComponent(ContextMenu);

    const replyId = '6905754b-554e-44f7-9553-8d622710e303';
    const editReplyContent = 'Rosalution is the best.';

    contextMenu.vm.$emit('edit', replyId);
    await wrapper.vm.$nextTick();

    const discussionReply = wrapper.getComponent(DiscussionReply);

    const editReplyTextArea = discussionReply.find('[data-test=discussion-reply-edit-text-area]');
    await editReplyTextArea.setValue(editReplyContent);

    const editReplySaveButton = discussionReply.find('[data-test=edit-discussion-reply-save]');
    editReplySaveButton.trigger('click');
    await wrapper.vm.$nextTick();

    const emittedObject = wrapper.emitted()['reply:edit'][0];

    expect(emittedObject[0]).toBe(replyId);
    expect(emittedObject[1]).toBe(editReplyContent);
  });

  it('Should recieve an emit to edit a post and cancels the edit post dialog closing the edit field', async () => {
    const wrapper = getMountedComponent({userClientId: 'fake-user-id'});

    const contextMenu = wrapper.getComponent(ContextMenu);

    const replyId = '6905754b-554e-44f7-9553-8d622710e303';
    contextMenu.vm.$emit('edit', replyId);

    await wrapper.vm.$nextTick();

    const discussionReply = wrapper.getComponent(DiscussionReply);

    expect(discussionReply.vm.editingReplyFlag.value).toBe(true);

    const editReplyCancelButton = discussionReply.find('[data-test=edit-discussion-reply-cancel]');

    editReplyCancelButton.trigger('click');

    await wrapper.vm.$nextTick();

    expect(discussionReply.vm.editingReplyFlag.value).toBe(false);
  });
});
