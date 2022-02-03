import {test, expect} from 'vitest';
import {mount} from '@vue/test-utils';

import NavigationComponent from '../../src/components/NavigationComponent.vue';

// Skipping these tests due to the use of Vue Router.
// Running test without mocking result in following warnings:
// [Vue warn]: Failed to resolve component: router-view
// [Vue warn]: Failed to resolve component: router-link
// https://www.wrike.com/open.htm?id=837264942

test.skip('Vue instance exists and it is an object', () => {
  const wrapper = mount(NavigationComponent, {shallow: true});
  expect(typeof wrapper).toBe('object');
});
