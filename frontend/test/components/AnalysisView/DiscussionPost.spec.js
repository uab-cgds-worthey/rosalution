import {it, expect, describe} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import ContextMenu from '../../../src/components/ContextMenu.vue';
import DiscussionPost from '../../../src/components/AnalysisView/DiscussionPost.vue';
import DiscussionReply from '../../../src/components/AnalysisView/DiscussionReply.vue';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import DiscussionAttachment from '../../../src/components/AnalysisView/DiscussionAttachment.vue';

/**
 * Helper mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {
    id: '9027ec8d-6298-4afb-add5-6ef710eb5e98',
    key: '9027ec8d-6298-4afb-add5-6ef710eb5e98',
    authorId: 'fake-user-id',
    authorName: 'Developer Person',
    publishTimestamp: '2023-10-09T21:13:22.687000',
    content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse eget metus nec erat accumsan rutrum',
    attachments: [
      {
        'name': 'CGDS',
        'attachment_id': 'cb82fe13-4190-4faa-9108-905b62f97820',
        'data': 'https://sites.uab.edu/cgds/',
        'type': 'link',
      },
      {
        'name': 'Rosalution Github Repository',
        'attachment_id': '55f22661-a24e-4ef0-9152-df79b386b09a',
        'data': 'https://github.com/uab-cgds-worthey/rosalution',
        'type': 'link',
      },
    ],
    thread: [
      {
        replyId: '6905754b-554e-44f7-9553-8d622710e303',
        authorId: 'fake-user-id',
        authorName: 'Developer Person',
        publishTimestamp: '2024-10-09T21:13:22.687000',
        content: 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugit nulla paritur.',
        actions: [{text: 'Edit'}, {text: 'Delete'}],
      },
    ],
    actions: [{text: 'Edit'}, {text: 'Delete'}],
  };

  return shallowMount(DiscussionPost, {
    props: {...defaultProps, ...props},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
      },
    },
  });
}

describe('DiscussionPost.vue', () => {
  it('Vue instance exists and it is an object', () => {
    const wrapper = getMountedComponent();
    expect(typeof wrapper).to.not.be.undefined;
  });

  it('Should display a context menu for a user that authored a discussion post', () => {
    const wrapper = getMountedComponent({userClientId: 'fake-user-id'});

    const contextMenu = wrapper.find('[data-test=discussion-post-context-menu]');

    expect(contextMenu.exists()).toBe(true);
  });

  it('Should not display a context menu for a user that did not author the discussion post', () => {
    const wrapper = getMountedComponent({userClientId: 'different-fake-user-id'});

    const contextMenu = wrapper.find('[data-test=discussion-post-context-menu]');

    expect(contextMenu.exists()).toBe(false);
  });

  it('Should recieve an emit to delete a post and emits a post:delete with postId', async () => {
    const wrapper = getMountedComponent({userClientId: 'fake-user-id'});

    const postId = '9027ec8d-6298-4afb-add5-6ef710eb5e98';

    const contextMenu = wrapper.getComponent(ContextMenu);

    contextMenu.vm.$emit('delete', postId);

    await wrapper.vm.$nextTick();

    const emittedObject = wrapper.emitted()['post:delete'][0];

    expect(emittedObject[0]).toBe(postId);
  });

  it('Should recieve an emit to edit a post and emits a post:edit with the new message upon confirmation', async () => {
    const wrapper = getMountedComponent({userClientId: 'fake-user-id'});

    const contextMenu = wrapper.getComponent(ContextMenu);

    const testPostId = '9027ec8d-6298-4afb-add5-6ef710eb5e98';
    const testPostContent = 'Inuyasha is the best.';

    contextMenu.vm.$emit('edit', testPostId);

    await wrapper.vm.$nextTick();

    const discussionPost = wrapper.getComponent(DiscussionPost);

    await discussionPost.setData({editPostContent: testPostContent});

    const editPostSaveButton = discussionPost.find('[data-test=edit-discussion-save]');

    editPostSaveButton.trigger('click');

    await wrapper.vm.$nextTick();

    const emittedObject = wrapper.emitted()['post:edit'][0];

    expect(emittedObject[0]).toBe(testPostId);
    expect(emittedObject[1]).toBe(testPostContent);
  });

  it('Should recieve an emit to edit a post and cancels the edit post dialog closing the edit field', async () => {
    const wrapper = getMountedComponent({userClientId: 'fake-user-id'});

    const contextMenu = wrapper.getComponent(ContextMenu);

    const testPostId = '9027ec8d-6298-4afb-add5-6ef710eb5e98';

    contextMenu.vm.$emit('edit', testPostId);

    await wrapper.vm.$nextTick();

    const discussionPost = wrapper.getComponent(DiscussionPost);

    expect(discussionPost.vm.editingPostFlag).toBe(true);

    const editPostCancelButton = discussionPost.find('[data-test=edit-discussion-cancel]');

    editPostCancelButton.trigger('click');

    await wrapper.vm.$nextTick();

    expect(discussionPost.vm.editingPostFlag).toBe(false);
  });

  it('Should emit a discussion:new-reply event when the publish reply button is pressed', async () => {
    const wrapper = getMountedComponent({userClientId: 'fake-user-id'});
    const newReplyContent = 'Test reply content.';

    const discussionPost = wrapper.getComponent(DiscussionPost);

    const newDiscussionReplyButton = wrapper.find('[data-test=discussion-new-reply-button]');
    await newDiscussionReplyButton.trigger('click');

    const newReplyTextArea = discussionPost.find('[data-test=discussion-new-reply-text-area]');
    await newReplyTextArea.setValue(newReplyContent);

    const publishNewDiscussionReplyButton = wrapper.find('[data-test=discussion-new-reply-publish]');
    await publishNewDiscussionReplyButton.trigger('click');

    await wrapper.vm.$nextTick();

    const emittedObjects = wrapper.emitted()['discussion:new-reply'][0];

    expect(emittedObjects[1]).to.include('Test reply content');
  });

  it('Should not be able to publish a reply if the new reply content field is empty', async () => {
    const wrapper = getMountedComponent({userClientId: 'fake-user-id'});

    const newDiscussionReplyButton = wrapper.find('[data-test=discussion-new-reply-button]');
    await newDiscussionReplyButton.trigger('click');

    const publishNewDiscussionReplyButton = wrapper.find('[data-test=discussion-new-reply-publish]');
    expect(publishNewDiscussionReplyButton.attributes().disabled).to.not.be.undefined;
  });

  it('Should close the new discussion reply field when the cancel button is pressed', async () => {
    const wrapper = getMountedComponent({userClientId: 'fake-user-id'});

    const newDiscussionReplyButton = wrapper.find('[data-test=discussion-new-reply-button]');
    await newDiscussionReplyButton.trigger('click');

    const newDiscussionReplyCancelButton = wrapper.find('[data-test=new-discussion-reply-cancel-button]');

    await newDiscussionReplyCancelButton.trigger('click');

    await wrapper.vm.$nextTick();

    expect((wrapper.find('[data-test=discussion-new-reply-text-area]')).exists()).to.be.false;
  });

  it('Should clear the new discussion reply field content when it is cancelled from publishing', async () => {
    const wrapper = getMountedComponent({userClientId: 'fake-user-id'});

    const newDiscussionReplyButton = wrapper.find('[data-test=discussion-new-reply-button]');
    await newDiscussionReplyButton.trigger('click');

    const newReplyContent = 'Test reply content.';
    const newReplyTextArea = wrapper.find('[data-test=discussion-new-reply-text-area]');
    await newReplyTextArea.setValue(newReplyContent);

    const newDiscussionReplyCancelButton = wrapper.find('[data-test=new-discussion-reply-cancel-button]');

    await newDiscussionReplyCancelButton.trigger('click');

    await wrapper.vm.$nextTick();

    expect(wrapper.vm.newReplyContent).not.toBe(newReplyContent);
  });

  it('Should recieve an emit to edit reply and then emit discussion:edit-reply with reply id and content', async () => {
    const wrapper = getMountedComponent({userClientId: 'fake-user-id'});

    const discussionThread = wrapper.findAllComponents(DiscussionReply);

    const discussionPostId = '9027ec8d-6298-4afb-add5-6ef710eb5e98';
    const editReplyId = '6905754b-554e-44f7-9553-8d622710e303';
    const editReplyContent = 'Hermione Granger is the smartest!';

    discussionThread[0].vm.$emit('reply:edit', editReplyId, editReplyContent);

    await wrapper.vm.$nextTick();

    const emittedObject = wrapper.emitted()['discussion:edit-reply'][0];

    expect(emittedObject[0]).toBe(discussionPostId);
    expect(emittedObject[1]).toBe(editReplyId);
    expect(emittedObject[2]).toBe(editReplyContent);
  });

  it('Should recieve an emit to delete reply and then emit discussion:delete-reply with reply id', async () => {
    const wrapper = getMountedComponent({userClientId: 'fake-user-id'});

    const discussionThread = wrapper.findAllComponents(DiscussionReply);

    const discussionPostId = '9027ec8d-6298-4afb-add5-6ef710eb5e98';
    const deleteReplyId = '6905754b-554e-44f7-9553-8d622710e303';

    discussionThread[0].vm.$emit('reply:delete', deleteReplyId);

    await wrapper.vm.$nextTick();

    const emittedObject = wrapper.emitted()['discussion:delete-reply'][0];

    expect(emittedObject[0]).toBe(discussionPostId);
    expect(emittedObject[1]).toBe(deleteReplyId);
  });

  it('Should show new attachments in the action row in a new discussion post', async () => {
    const wrapper = getMountedComponent({userClientId: 'fake-user-id'});

    const discussionAttachments = wrapper.findAllComponents(DiscussionAttachment);

    expect(discussionAttachments.length).toBe(2);
  });
});
