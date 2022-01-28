import {test, expect} from 'vitest';
import {mount} from '@vue/test-utils';

import About from '../../src/views/AboutView.vue';

test('Vue instance exists and it is an object', () => {
  const wrapper = mount(About, {shallow: true});
  expect(typeof wrapper).toBe('object');
});
