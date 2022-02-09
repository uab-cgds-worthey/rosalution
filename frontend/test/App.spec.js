import {test, expect} from 'vitest';
import {mount} from '@vue/test-utils';

import {createRouter, createWebHistory} from 'vue-router';

import App from '../src/App.vue';
import Navigation from '../src/components/NavigationComponent.vue';
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

  const wrapper = mount(App, {
    global: {
      plugins: [router],
    },
  });

  expect(wrapper.find('app-sidebar').exists()).toBe(true);

  const sidebarNavComponent = wrapper.findComponent(Navigation);

  expect(sidebarNavComponent).toBeTruthy;
});
