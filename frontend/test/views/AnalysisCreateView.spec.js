import {expect} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import AnalysisCreateView from '../../src/views/AnalysisCreateView.vue';

test('Vue instance exists and it is an object', () => {
    const wrapper = shallowMount(AnalysisCreateView);
    expect(typeof wrapper).toBe('object');
});