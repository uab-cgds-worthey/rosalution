import {test, expect} from 'vitest';
import {mount} from '@vue/test-utils';

import App from '../src/App.vue';
// import AnalysisListing from '../src/views/AnalysisListing.vue';

test('Vue instance exists and it is an object', () => {
  const wrapper = mount(App, { shallow: true });
  expect(typeof wrapper).toBe('object');
});

// test('renders props.msg when passed', () => {
//   const msg = 'Listing of Analyses';
//   const wrapper = shallowMount(AnalysisListing, {
//     props: {msg},
//   });
//   expect(wrapper.html()).to.include(msg);
// });
