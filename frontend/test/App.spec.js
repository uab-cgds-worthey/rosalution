import {test, expect} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import {createRouter, createWebHistory} from 'vue-router';

import App from '../src/App.vue';
import AnalysisListingView from '../src/views/AnalysisListingView.vue';

test('Contains a the <router-view> to display the application with routes', () => {
  const router = createRouter({
    history: createWebHistory(),
    routes: [
      {
        path: '/',
        component: AnalysisListingView,
      },
    ],
  });

  const wrapper = shallowMount(App, {
    global: {
      plugins: [router],
      stubs: {
        NavigationComponent: true,
      },
    },
  });

  expect(wrapper.find('router-view-stub').exists()).toBe(true);
});
