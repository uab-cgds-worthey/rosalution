import {expect, describe, it, beforeAll, afterAll} from 'vitest';
import {config, shallowMount} from '@vue/test-utils';

import AnalysisCard from '@/components/AnalysisListing/AnalysisCard.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import {RouterLink} from 'vue-router';

/**
 * helper function that shallow mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {
    name: 'CPAM0046',
    description: 'LMNA-related congenital muscular dystropy',
    genomic_units: [
      {
        gene: 'LMNA',
        transcripts: ['NM_001017980.3'],
        variants: ['c.745C>T'],
      },
    ],
    nominated_by: 'Dr. Person Two',
    latest_status: 'Approved',
    created_date: '2021-09-30',
    last_modified_date: '2021-10-01',
  };

  return shallowMount(AnalysisCard, {
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
  config.global.renderStubDefaultSlot = true;
});

afterAll(() => {
  config.global.renderStubDefaultSlot = false;
});

describe('AnalysisCard.vue', () => {
  it('should show the analysis name', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.html()).to.contains('CPAM0046');
  });

  it('should show when the case was created', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.html()).to.contains('2021-09-30');
  });

  it('should show the date a sample in the case was last modified', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.text()).to.contains('2021-10-01');
  });

  it('should show the nominator information of the case', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.html()).to.contains('Dr. Person Two');
  });

  describe('should show the genomic units of the case', () => {
    it('should show the gene information for a case', () => {
      const wrapper = getMountedComponent();
      expect(wrapper.html()).to.contains('Gene');
      expect(wrapper.html()).to.contains('LMNA');
    });
    it('should show the transcript information for a case', () => {
      const wrapper = getMountedComponent();
      expect(wrapper.html()).to.contains('Transcript');
      expect(wrapper.html()).to.contains('NM_001017980.3');
    });
    it('should show the coordinates information for a case', () => {
      const wrapper = getMountedComponent();
      expect(wrapper.html()).to.contains('c.745C>T');
    });
  });

  it('uses an icon to display the current workflow status of an analysis', () => {
    [
      {
        latest_status: 'Approved',
        expected: 'check',
      },
      {
        latest_status: 'Declined',
        expected: 'x',
      },
      {
        latest_status: 'Ready',
        expected: 'clipboard-check',
      },
    ].forEach((test) => {
      const wrapper = getMountedComponent({
        latest_status: test.latest_status,
      });
      const icon = wrapper.get('font-awesome-icon-stub');
      expect(icon.attributes().icon).to.equal(test.expected);
    });
  });
});
