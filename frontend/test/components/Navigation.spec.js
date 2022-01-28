import {test, expect} from 'vitest';
import {mount} from '@vue/test-utils';

import Navigation from '../../src/components/Navigation.vue';

test('Vue instance exists and it is an object', () => {
  const wrapper = mount(Navigation, { shallow: true });
  expect(typeof wrapper).toBe('object');
});
