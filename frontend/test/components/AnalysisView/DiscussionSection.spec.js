import {it, expect, describe, beforeEach} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import DiscussionSection from '../../../src/components/AnalysisView/DiscussionSection.vue';
import DiscussionPost from '../../../src/components/AnalysisView/DiscussionPost.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import InputDialogAttachUrl from '../../../src/components/Dialogs/InputDialogAttachUrl.vue';
import InputDialog from '../../../src/components/Dialogs/InputDialog.vue';
import InputDialogExistingAttachments from '../../../src/components/Dialogs/InputDialogExistingAttachments.vue';
import DiscussionAttachment from '../../../src/components/AnalysisView/DiscussionAttachment.vue';

describe('DiscussionSection.vue', () => {
  let wrapper;

  beforeEach((props) => {
    const defaultProps = fixtureData();
    wrapper = shallowMount(DiscussionSection, {
      props: {...defaultProps, ...props},
      global: {
        components: {
          'font-awesome-icon': FontAwesomeIcon,
        },
      },
    });
  });

  it('Vue instance exists and it is an object', () => {
    expect(typeof wrapper).toBe('object');
  });

  it('Should contain 3 discussion posts', () => {
    const discussionPosts = wrapper.findAllComponents(DiscussionPost);

    expect(discussionPosts.length).toBe(3);
  });

  it('Should emit a discussion:new-post event when the publish button is pressed', async () => {
    await wrapper.setData({newPostContent: 'Test post content'});

    const newDiscussionButton = wrapper.find('[data-test=new-discussion-button]');
    await newDiscussionButton.trigger('click');

    const publishNewDiscussionButton = wrapper.find('[data-test=new-discussion-publish]');
    await publishNewDiscussionButton.trigger('click');

    const emittedObjects = wrapper.emitted()['discussion:new-post'][0];

    expect(emittedObjects[0]).to.include('Test post content');
  });

  it('Should not be able to publish a post if the new post content field is empty', async () => {
    const newDiscussionButton = wrapper.find('[data-test=new-discussion-button]');
    await newDiscussionButton.trigger('click');

    const publishNewDiscussionButton = wrapper.find('[data-test=new-discussion-publish]');
    expect(publishNewDiscussionButton.attributes().disabled).to.not.be.undefined;
  });

  it('Should close the new discussion post field when the cancel button is pressed', async () => {
    const newDiscussionButton = wrapper.find('[data-test=new-discussion-button]');
    await newDiscussionButton.trigger('click');

    const newDiscussionCancelButton = wrapper.find('[data-test=new-discussion-cancel]');

    await newDiscussionCancelButton.trigger('click');
  });

  it('Should recieve an emit to delete a post and then emit discussion:delete-post with the post id', async () => {
    const discussionPosts = wrapper.findAllComponents(DiscussionPost);

    const postId = '9027ec8d-6298-4afb-add5-6ef710eb5e98';

    discussionPosts[0].vm.$emit('post:delete', postId);

    await wrapper.vm.$nextTick();

    const emittedObject = wrapper.emitted()['discussion:delete-post'][0];

    expect(emittedObject[0]).toBe(postId);
  });

  it('Should recieve an emit to edit a post and then emit discussion:edit-post with post id and content', async () => {
    const discussionPosts = wrapper.findAllComponents(DiscussionPost);

    const editPostId = '9027ec8d-6298-4afb-add5-6ef710eb5e98';
    const editPostContent = 'No! Sailor Moon is the best!';

    discussionPosts[0].vm.$emit('post:edit', editPostId, editPostContent);

    await wrapper.vm.$nextTick();

    const emittedObject = wrapper.emitted()['discussion:edit-post'][0];

    expect(emittedObject[0]).toBe(editPostId);
    expect(emittedObject[1]).toBe(editPostContent);
  });

  it('Should recieve an emit to add new reply, then emit discussion:new-reply with post id and content', async () => {
    const discussionPosts = wrapper.findAllComponents(DiscussionPost);

    const postId = '9027ec8d-6298-4afb-add5-6ef710eb5e98';
    const newReplyContent = 'Hermione Granger is the smartest!';

    discussionPosts[0].vm.$emit('discussion:new-reply', postId, newReplyContent);
    await wrapper.vm.$nextTick();

    const emittedObject = wrapper.emitted()['discussion:new-reply'][0];

    expect(emittedObject[0]).toBe(postId);
    expect(emittedObject[1]).toBe(newReplyContent);
  });

  it('Should recieve an emit to edit reply and then emit discussion:edit-reply with reply id and content', async () => {
    const discussionPosts = wrapper.findAllComponents(DiscussionPost);

    const postId = '9027ec8d-6298-4afb-add5-6ef710eb5e98';
    const replyId = '6905754b-554e-44f7-9553-8d622710e303';
    const editReplyContent = 'Hermione Granger is the smartest!';

    discussionPosts[0].vm.$emit('discussion:edit-reply', postId, replyId, editReplyContent);
    await wrapper.vm.$nextTick();

    const emittedObject = wrapper.emitted()['discussion:edit-reply'][0];

    expect(emittedObject[0]).toBe(postId);
    expect(emittedObject[1]).toBe(replyId);
    expect(emittedObject[2]).toBe(editReplyContent);
  });

  it('Should recieve an emit to delete reply and then emit discussion:delete-reply with reply id', async () => {
    const discussionPosts = wrapper.findAllComponents(DiscussionPost);

    const postId = '9027ec8d-6298-4afb-add5-6ef710eb5e98';
    const replyId = '6905754b-554e-44f7-9553-8d622710e303';

    discussionPosts[0].vm.$emit('discussion:delete-reply', postId, replyId);
    await wrapper.vm.$nextTick();

    const emittedObject = wrapper.emitted()['discussion:delete-reply'][0];

    expect(emittedObject[0]).toBe(postId);
    expect(emittedObject[1]).toBe(replyId);
  });

  it('Should add a new attachment to a post when a new post is being created', async () => {
    await wrapper.setData({newPostContent: 'Test post content'});


    const newDiscussionButton = wrapper.find('[data-test=new-discussion-button]');
    await newDiscussionButton.trigger('click');

    const discussionAttachButton = wrapper.find('[data-test=discussion-attachment-button]');
    // console.log(discussionAttachButton.html());
    await discussionAttachButton.trigger('click');

    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();


    console.log(wrapper.html());

    // await wrapper.find('[data-test=button-input-dialog-attach-url]').trigger('click');
    // const attachUrlComponent = wrapper.findComponent(InputDialogAttachUrl);
    // expect(attachUrlComponent.exists()).to.be.true;

    // const attachment = {
    //   data: 'www.google.com',
    //   name: 'Test Link',
    //   type: 'link',
    // };

    // await wrapper.setData({newAttachments: [attachment]});

    // const discussionAttachment = wrapper.findAllComponents(DiscussionAttachment);
    // expect(discussionAttachment.length).toBe(1);
  });
});

/**
 * Returns fixture data
 * @return {Object} containing discussion data from CPAM0002.
 */
function fixtureData() {
  return {
    userClientId: 'fake-user-id',
    discussions: [
      {
        'post_id': '9027ec8d-6298-4afb-add5-6ef710eb5e98',
        'author_id': '3bghhsmnyqi6uxovazy07ryn9q1tqbnt',
        'author_fullname': 'Developer Person',
        'publish_timestamp': '2023-10-09T21:13:22.687000',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
        'attachments': [
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
        'thread': [
          {
            replyId: '6905754b-554e-44f7-9553-8d622710e303',
            authorId: 'fake-user-id',
            authorName: 'Developer Person',
            publishTimestamp: '2024-10-09T21:13:22.687000',
            content: 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugit paritur.',
            actions: [{text: 'Edit'}, {text: 'Delete'}],
          },
        ],
      },
      {
        'post_id': 'a677bb36-acf8-4ff9-a406-b113a7952f7e',
        'author_id': 'kw0g790fdx715xsr1ead2jk0pqubtlyz',
        'author_fullname': 'Researcher Person',
        'publish_timestamp': '2023-10-10T21:13:22.687000',
        'content': 'Mauris at mauris eu neque varius suscipit.',
        'attachments': [],
        'thread': [],
      },
      {
        'post_id': 'e6023fa7-b598-416a-9f42-862c826255ef',
        'author_id': 'exqkhvidr7uh2ndslsdymbzfbmqjlunk',
        'author_fullname': 'Variant Review Report Preparer Person',
        'publish_timestamp': '2023-10-13T21:13:22.687000',
        'content': 'Mauris at mauris eu neque varius suscipit.',
        'attachments': [],
        'thread': [],
      },
    ],
    supporting_evidence_files: [
      {
        'name': 'VMA21 deficiency prevents vacuolar ATPase assembly and causes autophagic vacuolar myopathy',
        'data': 'https://link.springer.com/article/10.1007/s00401-012-1073-6',
        'attachment_id': '19684b36-6e06-4659-93bb-6c420601d1da',
        'type': 'link',
        'comments': '',
      },
    ],
    actions: [
      {
        icon: 'xmark',
        text: 'Delete',
        emit: 'delete',
        operation: () => {},
      },
    ],
  };
}
