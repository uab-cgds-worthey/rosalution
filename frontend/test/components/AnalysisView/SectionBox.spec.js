import {expect, describe, it, beforeAll, afterAll} from 'vitest';
import {config, shallowMount} from '@vue/test-utils';

import SectionBox from '@/components/AnalysisView/SectionBox.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import {RouterLink} from 'vue-router';

/**
 * helper function that shallow mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {
    analysis_name: 'CPAM0046',
    header: 'Brief',
    contentList: [
      {
        field: 'Nominated',
        value: [
          'Dr. Person Two (Local) - working with Dr. Person Three in Person Four Lab',
        ],
      },
      {
        field: 'Reason',
        value: [
          'Contribute a dominant negative patient-variant model to the existing zebrafish model (LOF; in-progress)',
          'Will be used in NBL 240: a research-based undergraduate course at UAB',
        ],
      },
      {
        field: 'Desired Outcomes',
        value: [
          'Functional impact confirmation (animal/cell modeling)',
          'Therapeutic predictions (in-silico predictions)',
          'Downstream applications (sharing model to conduct larger drug screens)',
        ],
      },
    ],
  };

  return shallowMount(SectionBox, {
    props: {...defaultProps, ...props},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
        'router-link': RouterLink,
      },
    },
  });
}

beforeAll(() => {
  config.renderStubDefaultSlot = true;
});

afterAll(() => {
  config.renderStubDefaultSlot = false;
});

describe('SectionBox.vue', () => {
  it('should show Header name', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.text()).to.contains('Brief');
  });

  it('should show field names', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.text()).to.contains('Nominated');
    expect(wrapper.text()).to.contains('Reason');
    expect(wrapper.text()).to.contains('Desired Outcomes');
  });

  it('should show values', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.text()).to.contains('Dr. Person Two (Local) - working with Dr. Person Three in Person Four Lab');
  });
});
