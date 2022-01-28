import {test, expect} from 'vitest';
import {mount} from '@vue/test-utils';

import AnalysisListing from '../../src/views/AnalysisListing.vue';

test('Vue instance exists and it is an object', () => {
  const wrapper = mount(AnalysisListing, {shallow: true});
  expect(typeof wrapper).toBe('object');
});
