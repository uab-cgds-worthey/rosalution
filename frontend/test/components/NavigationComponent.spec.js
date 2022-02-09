import {expect, describe, beforeAll, it} from 'vitest';
import {createRouter, createWebHistory} from 'vue-router';
import {mount} from '@vue/test-utils';

import NavigationComponent from '../../src/components/NavigationComponent.vue';
import AnalysisListingView from '../../src/views/AnalysisListingView.vue';
import AnalysisCreateView from '../../src/views/AnalysisCreateView.vue';
import AboutView from '../../src/views/AboutView.vue';

describe('NavigationComponent.vue', () => {
  let wrapper;

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

  beforeAll(() => {
    wrapper = mount(NavigationComponent, {
      global: {
        plugins: [router],
      },
    });
  });

  it('Vue instance exists and it is an object', () => {
    expect(typeof wrapper).toBe('object');
  });

  it('Navigation bar has 1 nav tag', () => {
    const navTag = wrapper.findAll('nav');
    // Expecting only a single nav tag. Update when links are added.
    expect(navTag.length).toBe(1);
  });
});
