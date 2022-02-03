import {test, expect} from 'vitest';
import {mount} from '@vue/test-utils';

import AnalysisListingView from '../../src/views/AnalysisListingView.vue';

test('Vue instance exists and it is an object', () => {
  const wrapper = mount(AnalysisListingView, {shallow: true});
  expect(typeof wrapper).toBe('object');
});

test('Analysis Listing contains a header and content', () => {
  const wrapper = mount(AnalysisListingView, {shallow: true});

  const appHeader = wrapper.find('app-header');
  expect(appHeader.exists()).toBe(true);

  const appContent = wrapper.find('app-content');
  expect(appContent.exists()).toBe(true);
});
