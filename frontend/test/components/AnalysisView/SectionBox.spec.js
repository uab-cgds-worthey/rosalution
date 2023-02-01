import {expect, describe, it, beforeAll, afterAll} from 'vitest';
import {config, shallowMount} from '@vue/test-utils';

import SectionBox from '@/components/AnalysisView/SectionBox.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import sinon from 'sinon';


/**
 * helper function that shallow mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {
    analysis_name: 'CPAM0046',
    header: 'Brief',
    content: [
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
    edit: false,
  };

  return shallowMount(SectionBox, {
    props: {...defaultProps, ...props},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
      },
    },
  });
}

describe('SectionBox.vue', () => {
  let sandbox;

  beforeAll(() => {
    sandbox = sinon.createSandbox();
    config.global.renderStubDefaultSlot = true;
  });

  afterAll(() => {
    sandbox.restore();
    config.global.renderStubDefaultSlot = false;
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

    it('changes value fields to input fields if edit is toggled', () => {
      const wrapper = getMountedComponent({
        edit: true,
      });
      const valueInput = wrapper.find('[data-test=editable-value]');
      expect(valueInput.exists()).to.be.true;
    });

    it('displays values when edit is not toggled', () => {
      const wrapper = getMountedComponent();
      const values = wrapper.find('[data-test=value-row]');
      expect(values.exists()).to.be.true;
    });

    it('shows edit logo when edit mode is toggled', async () => {
      const wrapper = getMountedComponent({
        edit: true,
      });
      const editLogo = wrapper.find('[class=edit-logo]');
      expect(editLogo.exists()).to.be.true;
    });

    it('shows collapsable logo when edit mode is not toggled', () => {
      const wrapper = getMountedComponent();
      const collapsableLogo = wrapper.find('[class=collapsable-logo]');
      expect(collapsableLogo.exists()).to.be.true;
    });

    it('shows an image if the pedigree section has one returned', async () => {
      const wrapper = getMountedComponent({
        analysis_name: 'CPAM0046',
        header: 'Pedigree',
        content: [{field: 'image', value: ['fakeimagefileid']}],
      });

      const pedigreeImageTag = wrapper.find('img');

      expect(pedigreeImageTag.html()).to.contain('/rosalution/api/analysis/download/fakeimagefileid');
    });
  });
});
