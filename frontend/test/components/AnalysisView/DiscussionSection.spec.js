import {it, expect, describe, beforeEach} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import DiscussionSection from '../../../src/components/AnalysisView/DiscussionSection.vue';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

describe('DiscussionSection.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(DiscussionSection, {
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
});
