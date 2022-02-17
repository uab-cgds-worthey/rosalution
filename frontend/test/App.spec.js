import {test, expect} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import {createRouter, createWebHistory} from 'vue-router';

import App from '../src/App.vue';
import AnalysisListingView from '../src/views/AnalysisListingView.vue';
import AnalysisCreateView from '../src/views/AnalysisCreateView.vue';
import AboutView from '../src/views/AboutView.vue';

test('Contains a <sidebar> tag with a <navigation> component', () => {
  const router = createRouter({
    history: createWebHistory(),
    routes: [
      {
        path: '/',
        component: AnalysisListingView,
      },
      {
        path: '/analysis/create',
        component: AnalysisCreateView,
      },
      {
        path: '/about',
        component: AboutView,
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

  expect(wrapper.find('app-sidebar').exists()).toBe(true);
  expect(wrapper.find('navigation-component-stub').exists()).toBe(true);
});
