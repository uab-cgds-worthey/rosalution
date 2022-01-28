import {test, expect} from 'vitest';
import {mount} from '@vue/test-utils';

import NavigationComponent from '../../src/components/NavigationComponent.vue';

test('Vue instance exists and it is an object', () => {
  const wrapper = mount(NavigationComponent, {shallow: true});
  expect(typeof wrapper).toBe('object');
});
