import {test, expect} from 'vitest';
import {mount} from '@vue/test-utils';

import AnalysisListingView from '../../src/views/AnalysisListingView.vue';

test('Vue instance exists and it is an object', () => {
  const wrapper = mount(AnalysisListingView, {shallow: true});
  expect(typeof wrapper).toBe('object');
});
