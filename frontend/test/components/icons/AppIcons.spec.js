import {describe, it, expect} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import AppIcons from '../../../src/components/icons/AppIcons.vue';

/**
   * This function creates a shallow mount for the vue component
   * @param {Object} propsData Mocked props data
   * @return {Object} shallowMount to be used
   */
function getMountedComponent(propsData) {
  const defaultPropsData = {
    type: 'calendar',
  };

  return shallowMount(AppIcons, {
    propsData: {...defaultPropsData, ...propsData},
  });
}

describe('icon.vue', () => {
  it('should render the specified icon', async () => {
    const wrapper = getMountedComponent();

    const calendarPartialCoords = `M17,3h-1v2h-3V3H7v2H4V3H3C1.899,3,1,3.9,1,5v12c0,1.1,0.899,2,2,2h14c1.1,0`;

    expect(wrapper.vm.viewableIcon).to.contain(calendarPartialCoords);
  });


  it('if icon does not exist then return a default', () => {
    const wrapper = getMountedComponent({type: 'not-a-icon'});
    expect(wrapper.vm.viewableIcon).to.contain(`d="M202.021 0C122.202 0 70.503 32.703 29.914 91.026c-7.363`);
  });
});
