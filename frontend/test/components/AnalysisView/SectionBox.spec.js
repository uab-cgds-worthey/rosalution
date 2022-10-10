import {expect, describe, it, beforeAll, afterAll} from 'vitest';
import {config, shallowMount} from '@vue/test-utils';

import Analyses from '@/models/analyses.js';
import SectionBox from '@/components/AnalysisView/SectionBox.vue';
import SectionImportModal from '@/components/AnalysisView/SectionImportModal.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import {RouterLink} from 'vue-router';
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
        'router-link': RouterLink,
      },
    },
  });
}

describe('SectionBox.vue', () => {
  let sandbox;

  beforeAll(() => {
    sandbox = sinon.createSandbox();
    config.renderStubDefaultSlot = true;
  });

  afterAll(() => {
    sandbox.restore();
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

    it('changes value fields to input fields if edit is toggled', () => {
      const wrapper = getMountedComponent({
        edit: true,
      });
      const valueInput = wrapper.find('[data-test=editable-value]');
      expect(valueInput.exists()).to.be.true;
    });

    it('only displays values when edit is not toggled', () => {
      const wrapper = getMountedComponent();
      const values = wrapper.find('[data-test=value-row]');
      expect(values.exists()).to.be.true;
    });

    it('shows edit logo when edit mode is toggled', async () => {
      const wrapper = getMountedComponent({
        edit: true,
      });
      const editLogo = wrapper.find('[data-test=edit-logo]');
      expect(editLogo.exists()).to.be.true;
    });

    it('shows collapsable logo when edit mode is not toggled', () => {
      const wrapper = getMountedComponent();
      const collapsableLogo = wrapper.find('[data-test=collapsable-logo]');
      expect(collapsableLogo.exists()).to.be.true;
    });

    it('shows the attach section import modal when the paperclip is clicked', async () => {
      const wrapper = getMountedComponent({
        analysis_name: 'CPAM0046',
        header: 'Pedigree',
        content: [],
      });
      const sectionAttachModalButton = wrapper.find('[data-test=attach-logo]');

      expect(wrapper.vm.showModal).to.equal(false);

      await sectionAttachModalButton.trigger('click');

      expect(wrapper.vm.showModal).to.equal(true);
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

    it('accepts an image and sends a request to save it to mongo', async () => {
      const wrapper = getMountedComponent({
        analysis_name: 'CPAM0046',
        header: 'Pedigree',
        content: [],
      });

      const mockAttach = sinon.stub(Analyses, 'attachSectionBoxImage');
      mockAttach.returns(fixtureData);

      const spyAttach = sinon.spy(wrapper.vm, 'addSectionFile');

      const fakeImage = {name: 'fakeImage.png'};

      const sectionAttachModalButton = wrapper.find('[data-test=attach-logo]');
      await sectionAttachModalButton.trigger('click');

      const importModal = wrapper.getComponent(SectionImportModal);

      importModal.vm.$emit('add', fakeImage);

      expect(spyAttach.calledWith(fakeImage)).to.equal(true);
    });
  });
});


/**
 * Returns fixture data
 * @return {Object} containing analysis data for CPAM0046.
 */
function fixtureData() {
  return {
    name: 'CPAM0046',
    description: ': LMNA-related congenital muscular dystropy',
    nominated_by: 'Dr. Person Two',
    latest_status: 'Approved',
    created_date: '2021-09-30',
    last_modified_date: '2021-10-01',
    genomic_units: [{
      gene: 'LMNA',
      transcripts: [{transcript: 'NM_170707.3'}],
      variants: [{
        hgvs_variant: 'NM_170707.3:c.745C>T',
        c_dot: 'c.745C>T',
        p_dot: 'p.R249W',
        build: 'hg19',
        case: [
          {
            field: 'Evidence',
            value: ['PS2', 'PS3', 'PM2', 'PP3', 'PP5'],
          },
          {
            field: 'Interpretation',
            value: ['Pathogenic'],
          },
          {
            field: 'Inheritance',
            value: ['De Novo'],
          },
        ],
      }],
    }],
    sections: [{
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
          value: ['Functional impact confirmation (animal/cell modeling)'],
        },
      ],
    }, {
      header: 'Medical Summary',
      content: [
        {
          field: 'Clinical Diagnosis',
          value: ['LMNA-related congenital muscular dystropy'],
        },
        {
          field: 'Affected Individuals Identified',
          value: ['Male, YOB: 2019'],
        },
      ],
    },
    {
      header: 'Pedigree',
      content: [{field: 'image', value: ['fakeimagefileid']}],
    },
    {
      header: 'Case Information',
      content: [{
        field: 'Systems',
        value: ['Growth Parameters; Craniofacial; Musculoskeletal; Gastrointestinal; Behavior, Cognition;'],
      }, {
        field: 'HPO Terms',
        value: ['HP:0001508; HP:0001357; HP:0000473; HP:0003560; HP:0003701; HP:0009062; HP:0012389; HP: 0003236;'],
      }, {
        field: 'Additional Details',
        value: [
          'Review of VUSes (Why not considered)',
          'NEB (NM_001164508.1)  | c.7385C>G (p.A2462G) (Pat.) and c.16625A>G (p.H5542R) (Mat.). ',
          'LYZL6 (NM_020426.2)  | c.228G>C (p.Q76H) (Mat./Pat.) - Lysozyme Like 6. - No currently known disease',
          'NOL6 (NM_022917.4)  | c.518G>A (p.R173Q) (Pat.) and c.91G>A (p.G31R) (Mat.). - Nucleolar protein 6. -',
        ],
      }, {
        field: 'Experimental Design',
        value: [],
      }, {
        field: 'Prior Testing',
        value: ['WES - February  2020;'],
      }],
    }],
  };
}
