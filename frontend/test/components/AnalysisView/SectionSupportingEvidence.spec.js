import {describe, it, expect} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import SectionSupportingEvidence from '@/components/AnalysisView/SectionSupportingEvidence.vue';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

/**
 * Helper mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultPropsData = {
    field: 'Vetrinary Pathology Report',
    value: [{
      'name': 'CPAM0046-NM_170707.3 (LMNA)_ c.745C_T (p.R249W) other 2.PDF',
      'attachment_id': '64dbcfa43d243bf1e782499f',
      'type': 'file',
      'comments': '',
    }],
    editable: true,
    writePermissions: true,
  };

  return shallowMount(SectionSupportingEvidence, {
    props: {...defaultPropsData, ...props},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
      },
    },
  });
}

describe('SectionSupportingEvidence.vue', () => {
  let wrapper;

  it('renders the supporting evidence when the value exists', async () => {
    wrapper = getMountedComponent();
    expect(wrapper.html()).to.include('CPAM0046');
  });

  it('renders an attach button when there is not content to render', () => {
    wrapper = getMountedComponent({
      value: [],
    });
    const attachButton = wrapper.find('[data-test="attach-button-Vetrinary Pathology Report"]');
    expect(attachButton.exists()).to.be.true;
  });
});
