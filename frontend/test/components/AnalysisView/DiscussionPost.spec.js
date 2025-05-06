import {it, expect, describe} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import ContextMenu from '../../../src/components/ContextMenu.vue';
import DiscussionPost from '../../../src/components/AnalysisView/DiscussionPost.vue';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

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
    attachments: [],
    thread: [],
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
});
