import {test, expect} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import AppIcons from '../../../src/components/icons/AppIcons.vue';

test('Vue instance exists and it is an object', () => {
  const wrapper = shallowMount(AppIcons, {
    props: {

    },
  });
  expect(typeof wrapper).toBe('object');
});
