import {it, expect, describe, beforeEach} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import DiscussionPost from '../../../src/components/AnalysisView/DiscussionPost.vue';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

describe('DiscussionPost.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(DiscussionPost, {
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
});
