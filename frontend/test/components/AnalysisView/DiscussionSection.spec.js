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
});
