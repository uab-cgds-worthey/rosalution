import {describe, it, expect, beforeAll} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import AnalysisListingView from '../../src/views/AnalysisListingView.vue';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

describe('AnalysisListingView', () => {
  let wrapper;

  beforeAll(() => {
    wrapper = shallowMount(AnalysisListingView, {
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

  it('Analysis Listing contains a header and content', () => {
    const appHeader = wrapper.find('app-header');
    expect(appHeader.exists()).toBe(true);

    const appContent = wrapper.find('app-content');
    expect(appContent.exists()).toBe(true);
  });
});
