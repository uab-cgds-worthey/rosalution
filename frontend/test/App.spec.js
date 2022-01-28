import {test, expect} from 'vitest';

import {shallowMount} from '@vue/test-utils';
import AnalysisListing from '../src/views/AnalysisListing.vue';

test('renders props.msg when passed', () => {
  const msg = 'Listing of Analyses';
  const wrapper = shallowMount(AnalysisListing, {
    props: {msg},
  });
  expect(wrapper.html()).to.include(msg);
});
