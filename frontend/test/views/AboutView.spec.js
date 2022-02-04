import {test, expect} from 'vitest';
import {mount} from '@vue/test-utils';

import AboutView from '../../src/views/AboutView.vue';

test('Vue instance exists and it is an object', () => {
  const wrapper = mount(AboutView, {shallow: true});
  expect(typeof wrapper).toBe('object');
});

test('Analysis Listing contains a header, content, and footer', () => {
  const wrapper = mount(AboutView, {shallow: true});

  const appHeader = wrapper.find('app-header');
  expect(appHeader.exists()).toBe(true);

  const appContent = wrapper.find('app-content');
  expect(appContent.exists()).toBe(true);

  const appFooter = wrapper.find('app-footer');
  expect(appFooter.exists()).toBe(true);
});
