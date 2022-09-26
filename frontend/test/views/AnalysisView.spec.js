import {expect, describe, it, beforeAll, afterAll, beforeEach} from 'vitest';
import {shallowMount} from '@vue/test-utils';
import sinon from 'sinon';

import Analyses from '@/models/analyses.js';
import Auth from '@/models/authentication.js';

import AnalysisView from '@/views/AnalysisView.vue';
import SupplementalFormList from '@/components/AnalysisView/SupplementalFormList.vue';
import RemoveFileConfirmationDialog from '@/components/AnalysisView/RemoveFileConfirmationDialog.vue';
import ModalDialog from '@/components/AnalysisView/ModalDialog.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import {RouterLink} from 'vue-router';


/**
 * Helper mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {analysis_name: 'CPAM0046'};

  return shallowMount(AnalysisView, {
    props: {...defaultProps, ...props},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
        'router-link': RouterLink,
      },
      mocks: {
        $route: {
          push: sinon.spy(),
        },
        $router: {
          push: sinon.spy(),
        },
      },
    },
  });
}


describe('AnalysisView', () => {
  let mockedData;
  let mockedUser;
  let mockedLogout;
  let wrapper;
  let sandbox;

  beforeAll(() => {
    sandbox = sinon.createSandbox();
    mockedData = sandbox.stub(Analyses, 'getAnalysis');
    mockedData.returns(fixtureData());

    mockedUser = sandbox.stub(Auth, 'getUser');
    mockedUser.returns('');

    mockedLogout = sandbox.stub(Auth, 'logout');
  });

  beforeEach(() => {
    wrapper = getMountedComponent();
  });

  afterAll(() => {
    sandbox.restore();
  });

  it('contains a header and content', () => {
    const appHeader = wrapper.find('app-header');
    expect(appHeader.exists()).toBe(true);

    const appContent = wrapper.find('app-content');
    expect(appContent.exists()).toBe(true);
  });

  it('provides the expected headings of sections to be used as anchors to header', () => {
    const headerComponent = wrapper.get('[data-test="analysis-view-header"]');
    expect(headerComponent.attributes('sectionanchors'))
        .to.equal('Brief,Medical Summary,Case Information,Supplemental Attachments');
  });

  it('displays the attachment modal when the supplemental form list requests dialog', async () => {
    const supplementalComponent = wrapper.getComponent(SupplementalFormList);
    supplementalComponent.vm.$emit('open-modal');

    await wrapper.vm.$nextTick();

    const attachmentDialog = wrapper.findComponent(ModalDialog);
    expect(attachmentDialog.exists()).to.be.true;
  });

  it('attachment dialog adds a new attachment to the analysis', async () => {
    const supplementalComponent = wrapper.getComponent(SupplementalFormList);
    expect(supplementalComponent.props('attachments').length).to.equal(0);

    supplementalComponent.vm.$emit('open-modal');
    await wrapper.vm.$nextTick();

    const attachmentDialog = wrapper.findComponent(ModalDialog);
    attachmentDialog.vm.$emit('add', {file: 'fake'});
    await wrapper.vm.$nextTick();

    expect(supplementalComponent.props('attachments').length).to.equal(1);
  });

  it('prompts a confirmation when an attachment is to be deleted', async () => {
    const fakeAttachment = {file: 'fake'};
    const supplementalComponent = wrapper.getComponent(SupplementalFormList);
    expect(supplementalComponent.props('attachments').length).to.equal(0);

    // Manually adding to the modal needs to be done at this time due to not
    // querying existing attachments for the analaysis being viewed yet yet
    supplementalComponent.vm.$emit('open-modal');
    await wrapper.vm.$nextTick();

    const attachmentDialog = wrapper.findComponent(ModalDialog);
    attachmentDialog.vm.$emit('add', fakeAttachment);
    await wrapper.vm.$nextTick();

    expect(supplementalComponent.props('attachments').length).to.equal(1);

    supplementalComponent.vm.$emit('delete', fakeAttachment);
    await wrapper.vm.$nextTick();

    const confirmationDialog = wrapper.findComponent(RemoveFileConfirmationDialog);
    expect( confirmationDialog.exists()).to.be.true;
  });

  it('can cancel deleting the attachment via the confirmation and not delete the attachment', async () => {
    const fakeAttachment = {file: 'fake'};
    const supplementalComponent = wrapper.getComponent(SupplementalFormList);
    expect(supplementalComponent.props('attachments').length).to.equal(0);

    // Manually adding to the modal needs to be done at this time due to not
    // querying existing attachments for the analaysis being viewed yet yet
    supplementalComponent.vm.$emit('open-modal');
    await wrapper.vm.$nextTick();

    const attachmentDialog = wrapper.findComponent(ModalDialog);
    attachmentDialog.vm.$emit('add', fakeAttachment);
    await wrapper.vm.$nextTick();

    expect(supplementalComponent.props('attachments').length).to.equal(1);

    supplementalComponent.vm.$emit('delete', fakeAttachment);
    await wrapper.vm.$nextTick();

    const confirmationDialog = wrapper.findComponent(RemoveFileConfirmationDialog);
    confirmationDialog.vm.$emit('cancel');
    await wrapper.vm.$nextTick();

    expect(supplementalComponent.props('attachments').length).to.equal(1);
  });

  it('confirmation removes the attachment to the analysis', async () => {
    const fakeAttachment = {file: 'fake'};
    const supplementalComponent = wrapper.getComponent(SupplementalFormList);
    expect(supplementalComponent.props('attachments').length).to.equal(0);

    // Manually adding to the modal needs to be done at this time due to not
    // querying existing attachments for the analaysis being viewed yet yet
    supplementalComponent.vm.$emit('open-modal');
    await wrapper.vm.$nextTick();

    const attachmentDialog = wrapper.findComponent(ModalDialog);
    attachmentDialog.vm.$emit('add', fakeAttachment);
    await wrapper.vm.$nextTick();

    expect(supplementalComponent.props('attachments').length).to.equal(1);

    supplementalComponent.vm.$emit('delete', fakeAttachment);
    await wrapper.vm.$nextTick();

    const confirmationDialog = wrapper.findComponent(RemoveFileConfirmationDialog);
    confirmationDialog.vm.$emit('delete');
    await wrapper.vm.$nextTick();

    expect(supplementalComponent.props('attachments').length).to.equal(0);
  });

  it('should logout when the analysis listing header emits the logout event', async () => {
    const headerComponent = wrapper.getComponent('[data-test=analysis-view-header]');
    headerComponent.vm.$emit('logout');
    await headerComponent.vm.$nextTick();

    expect(mockedLogout.called).to.be.true;
    expect(wrapper.vm.$router.push.called).to.be.true;
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
    }, {
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
