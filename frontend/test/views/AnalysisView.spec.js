import {expect, describe, it, afterEach, beforeEach} from 'vitest';
import {shallowMount} from '@vue/test-utils';
import sinon from 'sinon';

import Analyses from '@/models/analyses.js';

import InputDialog from '@/components/Dialogs/InputDialog.vue';
import NotificationDialog from '@/components/Dialogs/NotificationDialog.vue';
import SupplementalFormList from '@/components/AnalysisView/SupplementalFormList.vue';
import SaveModal from '@/components/AnalysisView/SaveModal.vue';

import inputDialog from '@/inputDialog.js';
import notificationDialog from '@/notificationDialog.js';
import toast from '@/toast.js';

import AnalysisView from '@/views/AnalysisView.vue';

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

/**
 * Helper triggers an action based on the action text
 * @param {VueWrapper} wrapper The Vue wrapper containing the component instance
 * @param {string} actionText The text of the action to trigger
 * @return {Promise} A promise that resolves when the action is triggered
 */
async function triggerAction(wrapper, actionText) {
  const headerComponent = wrapper.getComponent('[data-test=analysis-view-header]');
  const actionsProps = headerComponent.props('actions');
  for (const action of actionsProps) {
    if (action.text === actionText) {
      action.operation();
      break;
    }
  }
}

/**
 * Helper sets up a mocked wrapper with the given latest status and returns it
 * @param {string} latestStatus The latest status of the analysis to set
 * @param {object} mockedData The mocked data to be used
 * @return {Promise<VueWrapper>} A promise that resolves with the mocked Vue wrapper
 */
async function getMockedWrapper(latestStatus, mockedData) {
  const analysisData = fixtureData();
  analysisData.latest_status = latestStatus;
  mockedData.returns(analysisData);
  const wrapper = getMountedComponent();
  await wrapper.vm.$nextTick();
  return wrapper;
}


describe('AnalysisView', () => {
  let mockedData;
  let pedigreeAttachMock;
  let pedigreeUpdateMock;
  let pedigreeRemoveMock;
  let mockedAttachSupportingEvidence;
  let mockedRemoveSupportingEvidence;
  let mockedAttachThirdPartyLink;
  let markReadyMock;
  let markActiveMock;
  let updateAnalysisSectionsMock;
  let wrapper;
  let sandbox;

  beforeEach(() => {
    sandbox = sinon.createSandbox();
    mockedData = sandbox.stub(Analyses, 'getAnalysis');
    mockedData.returns(fixtureData());

    pedigreeAttachMock = sandbox.stub(Analyses, 'attachSectionImage');
    pedigreeUpdateMock = sandbox.stub(Analyses, 'updateSectionImage');
    pedigreeRemoveMock = sandbox.stub(Analyses, 'removeSectionImage');

    mockedAttachSupportingEvidence = sandbox.stub(Analyses, 'attachSupportingEvidence');
    mockedRemoveSupportingEvidence = sandbox.stub(Analyses, 'removeSupportingEvidence');
    mockedAttachThirdPartyLink = sandbox.stub(Analyses, 'attachThirdPartyLink');

    markReadyMock = sandbox.stub(Analyses, 'markAnalysisReady');
    markActiveMock = sandbox.stub(Analyses, 'markAnalysisActive');

    updateAnalysisSectionsMock = sandbox.stub(Analyses, 'updateAnalysisSections');

    wrapper = getMountedComponent();
  });

  afterEach(() => {
    sandbox.restore();
  });

  it('contains the expected content body element', () => {
    const appContent = wrapper.find('app-content');
    expect(appContent.exists()).to.be.true;
  });

  describe('the header', () => {
    it('contains a header element', () => {
      const appHeader = wrapper.find('app-header');
      expect(appHeader.exists()).to.be.true;
    });

    it('should logout on the header logout event', async () => {
      const headerComponent = wrapper.getComponent(
          '[data-test=analysis-view-header]',
      );
      headerComponent.vm.$emit('logout');
      await headerComponent.vm.$nextTick();

      expect(wrapper.vm.$router.push.called).to.be.true;
    });

    it('provides the expected headings of sections to be used as anchors', () => {
      const headerComponent = wrapper.get('[data-test="analysis-view-header"]');
      expect(headerComponent.attributes('sectionanchors')).to.equal(
          'Brief,Medical Summary,Pedigree,Case Information,Supporting Evidence',
      );
    });

    it('should mark an analysis as ready', async () => {
      const wrapper = await getMockedWrapper('Annotation', mockedData);

      await triggerAction(wrapper, 'Mark Ready');

      expect(markReadyMock.called).to.be.true;
    });

    it('should display success toast with correct message when marking analysis as ready', async () => {
      const wrapper = await getMockedWrapper('Annotation', mockedData);

      await triggerAction(wrapper, 'Mark Ready');

      expect(toast.state.active).to.be.true;
      expect(toast.state.type).to.equal('success');
      expect(toast.state.message).to.equal('Analysis marked as ready.');
    });

    it('should display error toast with correct message when marking analysis as ready fails', async () => {
      const wrapper = await getMockedWrapper('Annotation', mockedData);
      const error = new Error('Failed to mark analysis as ready');
      markReadyMock.throws(error);

      try {
        await triggerAction(wrapper, 'Mark Ready');
      } catch (error) {
        console.log(error);
      }
      expect(toast.state.active).to.be.true;
      expect(toast.state.type).to.equal('error');
      expect(toast.state.message).to.equal('Error marking analysis as ready.');
    });

    it('should mark an analysis as active', async () => {
      const wrapper = await getMockedWrapper('Ready', mockedData);

      await triggerAction(wrapper, 'Mark Active');

      expect(markActiveMock.called).to.be.true;
    });

    it('should display info toast with correct message when marking analysis as active', async () => {
      const wrapper = await getMockedWrapper('Ready', mockedData);

      await triggerAction(wrapper, 'Mark Active');

      expect(toast.state.active).to.be.true;
      expect(toast.state.type).to.equal('info');
      expect(toast.state.message).to.equal('The Mark Ready feature is not yet implemented.');
    });

    it('should display info toast with correct message when entering edit mode', async () => {
      const wrapper = getMountedComponent();

      await triggerAction(wrapper, 'Edit');

      expect(toast.state.active).to.be.true;
      expect(toast.state.type).to.equal('success');
      expect(toast.state.message).to.equal('Edit mode enabled.');
    });
    it('should display info toast with correct message when exiting edit mode', async () => {
      const wrapper = getMountedComponent();
      await wrapper.setData({edit: true});
      await triggerAction(wrapper, 'Edit');

      expect(toast.state.active).to.be.true;
      expect(toast.state.type).to.equal('info');
      expect(toast.state.message).to.equal('Edit mode disabled, & changes were not saved.');
    });
  });

  describe('third party links', () => {
    it('should render the input dialog when the attach monday link menu action is clicked', async () => {
      const headerComponent = wrapper.getComponent(
          '[data-test=analysis-view-header]',
      );
      const actionsProps = headerComponent.props('actions');

      for (const action of actionsProps) {
        if (action.text === 'Attach Monday.com') {
          action.operation();
        }
      }

      const mondayDialog = wrapper.findComponent(InputDialog);
      expect(mondayDialog.exists()).to.be.true;
    });

    it('should add a link to monday_com', async () => {
      const newAttachmentData = {
        data: 'https://monday.com',
        type: 'link',
      };
      const analysisWithMondayLink = fixtureData();
      analysisWithMondayLink['monday_com'] = 'https://monday.com';
      mockedAttachThirdPartyLink.returns(analysisWithMondayLink);

      wrapper = getMountedComponent();
      const headerComponent = wrapper.getComponent('[data-test=analysis-view-header]');
      const actionsProps = headerComponent.props('actions');

      for (const action of actionsProps) {
        if (action.text === 'Attach Monday.com') {
          action.operation();
        }
      }

      inputDialog.confirmation(newAttachmentData);

      await wrapper.vm.$nextTick();

      expect(mockedAttachThirdPartyLink.called).to.be.true;
    });

    it('should render the input dialog when the attach phenotips link menu action is clicked', async () => {
      const headerComponent = wrapper.getComponent(
          '[data-test=analysis-view-header]',
      );
      const actionsProps = headerComponent.props('actions');

      for (const action of actionsProps) {
        if (action.text === 'Connect PhenoTips') {
          action.operation();
        }
      }

      const phenotipsDialog = wrapper.findComponent(InputDialog);
      expect(phenotipsDialog.exists()).to.be.true;
    });

    it('should add a link to phenotips_com', async () => {
      const newAttachmentData = {
        data: 'https://phenotips.com',
        type: 'link',
      };
      const analysisWithPhenotipsLink = fixtureData();
      analysisWithPhenotipsLink['phenotips_com'] = 'https://phenotips.com';
      mockedAttachThirdPartyLink.returns(analysisWithPhenotipsLink);

      wrapper = getMountedComponent();
      const headerComponent = wrapper.getComponent('[data-test=analysis-view-header]');
      const actionsProps = headerComponent.props('actions');

      for (const action of actionsProps) {
        if (action.text === 'Connect PhenoTips') {
          action.operation();
        }
      }

      inputDialog.confirmation(newAttachmentData);

      await wrapper.vm.$nextTick();

      expect(mockedAttachThirdPartyLink.called).to.be.true;
    });
  });

  describe('supporting evidence', () => {
    describe('when adding supporting evidence as an attachment', () => {
      it('displays the attachment modal when the supplemental form list requests dialog', async () => {
        const supplementalComponent =
          wrapper.getComponent(SupplementalFormList);
        supplementalComponent.vm.$emit('open-modal');

        await wrapper.vm.$nextTick();

        const attachmentDialog = wrapper.findComponent(InputDialog);
        expect(attachmentDialog.exists()).to.be.true;
      });

      it('attachment dialog adds a new attachment to the analysis', async () => {
        const newAttachmentData = {
          name: 'fake-attachment-evidence-name',
          data: 'http://sites.uab.edu/cgds',
          attachment_id: 'new-failure-id',
          type: 'link',
          comments: '',
        };
        const analysisWithNewEvidence = fixtureData();
        analysisWithNewEvidence.supporting_evidence_files.push(
            newAttachmentData,
        );
        mockedAttachSupportingEvidence.returns(analysisWithNewEvidence);

        const supplementalComponent =
          wrapper.getComponent(SupplementalFormList);
        expect(supplementalComponent.props('attachments').length).to.equal(1);

        supplementalComponent.vm.$emit('open-modal');
        await wrapper.vm.$nextTick();

        inputDialog.confirmation(newAttachmentData);

        // Needs to cycle through updating the prop in the view and then another
        // tick for vuejs to reactively update the supplemental component
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();
        expect(supplementalComponent.props('attachments').length).to.equal(2);
      });
    });

    describe('when removing supporting evidence', async () => {
      it('prompts a confirmation when an attachment is to be deleted', async () => {
        const supplementalComponent =
          wrapper.getComponent(SupplementalFormList);
        expect(supplementalComponent.props('attachments').length).to.equal(1);

        const fakeAttachment = {name: 'fake.txt'};
        supplementalComponent.vm.$emit('delete', fakeAttachment);

        const confirmationDialog = wrapper.findComponent(NotificationDialog);
        expect(confirmationDialog.exists()).to.be.true;
      });

      it('can cancel deleting the attachment via the confirmation and not delete the attachment', async () => {
        const fakeAttachment = {name: 'fake.txt'};
        const supplementalComponent =
          wrapper.getComponent(SupplementalFormList);
        expect(supplementalComponent.props('attachments').length).to.equal(1);

        supplementalComponent.vm.$emit('delete', fakeAttachment);
        notificationDialog.cancel();

        expect(supplementalComponent.props('attachments').length).to.equal(1);
      });

      it('should confirmation to remove the supporting evidence from the analysis', async () => {
        const fakeAttachment = {name: 'fake.txt'};
        const supplementalComponent =
          wrapper.getComponent(SupplementalFormList);

        expect(supplementalComponent.props('attachments').length).to.equal(1);

        supplementalComponent.vm.$emit('delete', fakeAttachment);

        notificationDialog.confirmation();
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        expect(supplementalComponent.props('attachments').length).to.equal(0);
        expect(mockedRemoveSupportingEvidence.called).to.be.true;
      });

      it('should alert user when fails to delete', async () => {
        mockedRemoveSupportingEvidence.throws('Failed to delete');

        const fakeAttachment = {name: 'fake.txt'};
        const supplementalComponent =
          wrapper.getComponent(SupplementalFormList);

        expect(supplementalComponent.props('attachments').length).to.equal(1);

        supplementalComponent.vm.$emit('delete', fakeAttachment);

        notificationDialog.confirmation();
        await wrapper.vm.$nextTick();

        expect(supplementalComponent.props('attachments').length).to.equal(1);
        expect(mockedRemoveSupportingEvidence.called).to.be.true;
      });
    });
  });

  describe('sections', () => {
    describe('when an image section does not have an image', () => {
      it('accepts an image render as content', async () => {
        const newPedigreeSection = {
          header: 'Pedigree',
          content: [
            {
              field: 'image',
              value: ['fakeimagefileid'],
            },
          ],
        };
        pedigreeAttachMock.returns(newPedigreeSection);

        const pedigreeSection = wrapper.findComponent('[id=Pedigree]');
        pedigreeSection.vm.$emit('attach-image', 'Pedigree');
        await wrapper.vm.$nextTick();

        const fakeImage = {data: 'fakeImage.png'};
        inputDialog.confirmation(fakeImage);

        // Needs to cycle through updating the props in the view and then additional
        // ticks for vuejs to reactively update the supplemental component
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();
        const reRenderedPedigreeSection = wrapper.findComponent('[id=Pedigree]');

        expect(reRenderedPedigreeSection.props('content').length).to.equal(1);
      });
    });

    describe('when an image section has an image in it', () => {
      beforeEach(() => {
        const imageSection = {
          header: 'Pedigree',
          content: [{field: 'image', value: ['635a89aea7b2f21802b74539']}],
        };
        const analysisWithNewEvidence = fixtureData();
        const pedigreeSectionIndex =
          analysisWithNewEvidence.sections.findIndex((section) => section.header == 'Pedigree');
        analysisWithNewEvidence.sections.splice(pedigreeSectionIndex, 1, imageSection);
        mockedData.returns(analysisWithNewEvidence);
        wrapper = getMountedComponent();
      });

      it('updates section image content with input dialog', async () => {
        pedigreeUpdateMock.returns({
          header: 'Pedigree',
          content: [{field: 'image', value: ['different-image-635a89aea7b2f21802b74539']}],
        });

        const pedigreeSection = wrapper.findComponent('[id=Pedigree]');
        pedigreeSection.vm.$emit('update-image', 'Pedigree');
        await wrapper.vm.$nextTick();

        const fakeImageForUpdate = {data: 'fakeImage.png'};
        inputDialog.confirmation(fakeImageForUpdate);

        await wrapper.vm.$nextTick();

        const reRenderedPedigreeSection = wrapper.findComponent('[id=Pedigree]');

        expect(pedigreeUpdateMock.called).to.be.true;
        expect(reRenderedPedigreeSection.props('content').length).to.equal(1);
      });

      it('notifies user when updating section image content fails', async () => {
        pedigreeUpdateMock.throws('failure happened');

        const pedigreeSection = wrapper.findComponent('[id=Pedigree]');
        pedigreeSection.vm.$emit('update-image', 'Pedigree');
        await wrapper.vm.$nextTick();

        const fakeImageForUpdate = {data: 'fakeImage.png'};
        inputDialog.confirmation(fakeImageForUpdate);

        await wrapper.vm.$nextTick();

        const reRenderedPedigreeSection = wrapper.findComponent('[id=Pedigree]');

        const failureDialog = wrapper.findComponent(NotificationDialog);
        expect(failureDialog.exists()).to.be.true;

        expect(pedigreeUpdateMock.called).to.be.true;
        expect(reRenderedPedigreeSection.props('content').length).to.equal(1);
      });

      it('allows user to remove image content with input dialog with confirmation', async () => {
        pedigreeRemoveMock.resolves();

        const pedigreeSection = wrapper.findComponent('[id=Pedigree]');
        pedigreeSection.vm.$emit('update-image', 'Pedigree');
        await wrapper.vm.$nextTick();

        inputDialog.delete();

        await wrapper.vm.$nextTick();

        const confirmationDialog = wrapper.findComponent(NotificationDialog);
        expect(confirmationDialog.exists()).to.be.true;

        notificationDialog.confirmation();
        await wrapper.vm.$nextTick();

        // Neccesary to process several ticks to re-render the section
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        const reRenderedPedigreeSection = wrapper.findComponent('[id=Pedigree]');

        expect(pedigreeRemoveMock.called).to.be.true;
        expect(reRenderedPedigreeSection.props('content').length).to.equal(0);
      });

      it('notifies the user when the image content fails to be removed', async () => {
        pedigreeRemoveMock.throws('sad-it-did not remove');

        const pedigreeSection = wrapper.findComponent('[id=Pedigree]');
        pedigreeSection.vm.$emit('update-image', 'Pedigree');
        await wrapper.vm.$nextTick();

        inputDialog.delete();

        await wrapper.vm.$nextTick();

        notificationDialog.confirmation();
        await wrapper.vm.$nextTick();

        // Neccesary to process several ticks to re-render the section
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        const failureNotificationDialog = wrapper.findComponent(NotificationDialog);
        expect(failureNotificationDialog.exists()).to.be.true;
      });
    });
  });

  describe('Saving and canceling analysis changes displays toasts', () => {
    beforeEach(() => {
      updateAnalysisSectionsMock.resolves({sections: []});
    });

    it('should display success toast when saving analysis changes', async () => {
      const wrapper = getMountedComponent();
      await wrapper.setData({edit: true});
      const saveModal = wrapper.findComponent(SaveModal);

      saveModal.vm.$emit('save');
      await wrapper.vm.$nextTick();

      expect(toast.state.active).to.be.true;
      expect(toast.state.type).to.equal('success');
      expect(toast.state.message).to.equal('Analysis updated successfully.');
    });

    it('should display info toast when canceling analysis changes', async () => {
      const wrapper = getMountedComponent();
      await wrapper.setData({edit: true});
      const saveModal = wrapper.findComponent(SaveModal);

      saveModal.vm.$emit('canceledit');
      await wrapper.vm.$nextTick();

      expect(toast.state.active).to.be.true;
      expect(toast.state.type).to.equal('info');
      expect(toast.state.message).to.equal('Edit mode disabled, & changes were not saved.');
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
    third_party_links: [],
    genomic_units: [
      {
        gene: 'LMNA',
        transcripts: [{transcript: 'NM_170707.3'}],
        variants: [
          {
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
          },
        ],
      },
    ],
    sections: [
      {
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
      },
      {
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
        content: [],
      },
      {
        header: 'Case Information',
        content: [
          {
            field: 'Systems',
            value: [
              'Growth Parameters; Craniofacial; Musculoskeletal; Gastrointestinal; Behavior, Cognition;',
            ],
          },
          {
            field: 'HPO Terms',
            value: [
              'HP:0001508; HP:0001357; HP:0000473; HP:0003560; HP:0003701; HP:0009062; HP:0012389; HP: 0003236;',
            ],
          },
          {
            field: 'Additional Details',
            value: [
              'Review of VUSes (Why not considered)',
              'NEB (NM_001164508.1)  | c.7385C>G (p.A2462G) (Pat.) and c.16625A>G (p.H5542R) (Mat.). ',
              'LYZL6 (NM_020426.2)  | c.228G>C (p.Q76H) (Mat./Pat.) - Lysozyme Like 6. - No currently known disease',
              'NOL6 (NM_022917.4)  | c.518G>A (p.R173Q) (Pat.) and c.91G>A (p.G31R) (Mat.). - Nucleolar protein 6. -',
            ],
          },
          {
            field: 'Experimental Design',
            value: [],
          },
          {
            field: 'Prior Testing',
            value: ['WES - February  2020;'],
          },
        ],
      },
    ],
    supporting_evidence_files: [
      {
        name: 'fake.txt',
        attachment_id: 'fake-attachment-id',
        type: 'file',
        comments: '  ',
      },
    ],
  };
}
