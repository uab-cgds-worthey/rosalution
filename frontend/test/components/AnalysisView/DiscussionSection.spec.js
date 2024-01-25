import {it, expect, describe, beforeEach} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import DiscussionSection from '../../../src/components/AnalysisView/DiscussionSection.vue';
import DiscussionPost from '../../../src/components/AnalysisView/DiscussionPost.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

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
        'attachments': [],
        'thread': [],
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
