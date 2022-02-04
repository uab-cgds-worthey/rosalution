import {test, expect} from 'vitest';
import {mount} from '@vue/test-utils';

import App from '../src/App.vue';
import Navigation from '../src/components/NavigationComponent.vue';

// Skipping these tests due to the use of Vue Router.
// Running test without mocking result in following warnings:
// [Vue warn]: Failed to resolve component: router-view
// [Vue warn]: Failed to resolve component: router-link
// https://www.wrike.com/open.htm?id=837264942
test.skip('Vue instance exists and it is an object', () => {
  // function fakeRouterFunction() {
  //   return;
  // }

  const mockRoute = {
    params: {
      id: 1,
    },
  };

  const mockRouter = {
    // push: fakeRouterFunction(),
  };

  const wrapper = mount(App, {
    shallow: false,
    global: {
      mocks: {
        $route: mockRoute,
        $router: mockRouter,
      },
    },
  });

  expect(typeof wrapper).toBe('object');
});

test.skip('Contains a <sidebar> tag with a <navigation> component', () => {
  const wrapper = mount(App, {shallow: true});

  expect(wrapper.find('sidebar').exists()).toBe(true);

  const sidebarNavComponent = wrapper.findComponent(Navigation);

  expect(sidebarNavComponent).toBeTruthy;
});
