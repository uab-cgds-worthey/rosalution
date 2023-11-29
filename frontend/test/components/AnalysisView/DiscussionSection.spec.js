import {it, expect, describe, beforeEach, vi} from 'vitest';
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

    const publishNewDiscussionButton = wrapper.find('[data-test=new-discussion-publish]');
    await publishNewDiscussionButton.trigger('click');

    const emittedObjects = wrapper.emitted()['discussion:new-post'][0];

    expect(emittedObjects[0]).toBe('Test post content');
  });

  // Placeholder test
  it('Should print to console when the cancelled button is pressed', async () => {
    const cancelNewDiscussionButton = wrapper.find('[data-test=new-discussion-cancel]');

    vi.spyOn(console, 'log');
    await cancelNewDiscussionButton.trigger('click');
    expect(console.log).toHaveBeenCalled();
  });
});
