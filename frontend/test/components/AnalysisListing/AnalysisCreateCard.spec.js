import {expect, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import AnalysisCreateCard from '@/components/AnalysisListing/AnalysisCreateCard.vue';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

/**
 * helper function that shallow mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent() {
  return shallowMount(AnalysisCreateCard, {
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
      },
    },
  });
}

describe('AnalysisCreateCard.vue', () => {
  it('Should display a plus sign icon on the card', () => {
    const wrapper = getMountedComponent();
    const icon = wrapper.get('font-awesome-icon-stub');
    expect(icon.attributes().icon).to.equal('plus');
  });
});
