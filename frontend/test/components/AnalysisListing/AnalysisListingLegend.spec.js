import {expect, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import AnalysisListingLegend from '@/components/AnalysisListing/AnalysisListingLegend.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

const statuses = [
  {name: 'annotation', displayName: 'Annotating', icon: 'asterisk'},
  {name: 'ready', displayName: 'Ready', icon: 'clipboard-check'},
  {name: 'active', displayName: 'Active', icon: 'book-open'},
  {name: 'on-hold', displayName: 'On Hold', icon: 'pause'},
  {name: 'approved', displayName: 'Approved', icon: 'check'},
  {name: 'declined', displayName: 'Declined', icon: 'times'},
];

/**
 * helper function that shallow mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {
    statuses,
  };

  return shallowMount(AnalysisListingLegend, {
    props: {...defaultProps, ...props},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
      },
    },
  });
}

describe('AnalysisListingLegend.vue', () => {
  it('should display several states of rosalution analyses', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.html()).to.contains('Ready');
    expect(wrapper.html()).to.contains('Active');
  });

  it('should all be colored when no statuses are being filtered for', () => {
    const wrapper = getMountedComponent();
    statuses.forEach((status) => {
      expect(wrapper.html()).to.contains(`color: var(--rosalution-status-${status.name})`);
    });
  });

  it('should only color the filtered status', async () => {
    const wrapper = getMountedComponent();
    const statusElements = wrapper.findAll('.status');
    let readyStatus;

    for (let i = 0; i < statusElements.length; i++) {
      if (statusElements.at(i).text() === 'Ready') {
        readyStatus = statusElements.at(i);
      }
    }

    if (readyStatus) {
      await readyStatus.trigger('click');
      expect(wrapper.html()).to.contains('color: var(--rosalution-status-ready)');
      statuses.forEach((status) => {
        if (status.name !== 'ready') {
          expect(wrapper.html()).to.contains(`color: var(--rosalution-grey-300)`);
        }
      });
    } else {
      throw new Error('Ready status not found');
    }
  });

  it('should emit a filtered-statuses event when a status is clicked', async () => {
    const wrapper = getMountedComponent();
    const statusElements = wrapper.findAll('.status');
    let readyStatus;

    for (let i = 0; i < statusElements.length; i++) {
      if (statusElements.at(i).text() === 'Ready') {
        readyStatus = statusElements.at(i);
      }
    }

    if (readyStatus) {
      await readyStatus.trigger('click');
      expect(wrapper.emitted()).to.have.property('filtered-statuses');
      expect(wrapper.emitted()['filtered-statuses'][0][0]).to.contains('ready');
    } else {
      throw new Error('Ready status not found');
    }
  });
});
