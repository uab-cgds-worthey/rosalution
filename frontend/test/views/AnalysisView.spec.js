import {expect, describe, it, afterEach, beforeEach} from 'vitest';
import {shallowMount} from '@vue/test-utils';
import sinon from 'sinon';

import Analyses from '@/models/analyses.js';

import GeneBox from '@/components/AnalysisView/GeneBox.vue';
import InputDialog from '@/components/Dialogs/InputDialog.vue';
import NotificationDialog from '@/components/Dialogs/NotificationDialog.vue';
import DiscussionSection from '@/components/AnalysisView/DiscussionSection.vue';
import SupplementalFormList from '@/components/AnalysisView/SupplementalFormList.vue';
import SaveModal from '@/components/AnalysisView/SaveModal.vue';

import {authStore} from '@/stores/authStore.js';
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
  let attachSectionImageMock;
  let updateSectionImageMock;
  let removeSectionImageMock;
  let mockedAttachSupportingEvidence;
  let mockedRemoveSupportingEvidence;
  let mockedAttachThirdPartyLink;
  let markReadyMock;
  let updateAnalysisSectionsMock;
  let postNewDiscussionThreadMock;
  let mockAuthWritePermissions;
  let mockedAttachSectionSupportingEvidence;
  let mockedRemoveSectionSupportingEvidenceFile;
  let wrapper;
  let sandbox;

  beforeEach(() => {
    sandbox = sinon.createSandbox();
    mockedData = sandbox.stub(Analyses, 'getAnalysis');
    mockedData.returns(fixtureData());

    attachSectionImageMock = sandbox.stub(Analyses, 'attachSectionImage');
    updateSectionImageMock = sandbox.stub(Analyses, 'updateSectionImage');
    removeSectionImageMock = sandbox.stub(Analyses, 'removeSectionImage');

    mockedAttachSupportingEvidence = sandbox.stub(Analyses, 'attachSupportingEvidence');
    mockedRemoveSupportingEvidence = sandbox.stub(Analyses, 'removeSupportingEvidence');
    mockedAttachThirdPartyLink = sandbox.stub(Analyses, 'attachThirdPartyLink');

    mockedAttachSectionSupportingEvidence = sandbox.stub(Analyses, 'attachSectionSupportingEvidence');
    mockedRemoveSectionSupportingEvidenceFile = sandbox.stub(Analyses, 'removeSectionSupportingEvidenceFile');

    markReadyMock = sandbox.stub(Analyses, 'pushAnalysisEvent');

    updateAnalysisSectionsMock = sandbox.stub(Analyses, 'updateAnalysisSections');

    postNewDiscussionThreadMock = sandbox.stub(Analyses, 'postNewDiscussionThread');

    mockAuthWritePermissions = sandbox.stub(authStore, 'hasWritePermissions');
    mockAuthWritePermissions.returns(true);

    wrapper = getMountedComponent();
  });

  afterEach(() => {
    sandbox.restore();
  });

  it('contains the expected content body element', () => {
    const appContent = wrapper.find('app-content');
    expect(appContent.exists()).to.be.true;
  });

  it('should display a toast when a copy text to clipboard button', async () => {
    const geneBox = wrapper.getComponent(GeneBox);

    geneBox.vm.$emit('clipboard-copy', 'NM_001017980.3:c.164G>T');
    await wrapper.vm.$nextTick();

    expect(toast.state.active).to.be.true;
    expect(toast.state.type).to.equal('success');
    expect(toast.state.message).to.equal('Copied NM_001017980.3:c.164G>T to clipboard!');
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
          'Brief,Medical Summary,Mus musculus (Mouse) Model System,Pedigree,' +
          'Case Information,Discussion,Supporting Evidence',
      );
    });

    it('should mark an analysis as ready', async () => {
      const wrapper = await getMockedWrapper('Preparation', mockedData);

      await triggerAction(wrapper, 'Mark Ready');

      expect(markReadyMock.called).to.be.true;
    });

    it('should display success toast with correct message when marking analysis as ready', async () => {
      const wrapper = await getMockedWrapper('Preparation', mockedData);

      await triggerAction(wrapper, 'Mark Ready');

      expect(toast.state.active).to.be.true;
      expect(toast.state.type).to.equal('success');
      expect(toast.state.message).to.equal('Analysis event \'ready\' successful.');
    });

    it('should display error toast with correct message when marking analysis as ready fails', async () => {
      const wrapper = await getMockedWrapper('Preparation', mockedData);
      const error = new Error('Error updating the event \'ready\'.');
      markReadyMock.throws(error);

      try {
        await triggerAction(wrapper, 'Mark Ready');
      } catch (error) {
        console.error(error);
      }
      expect(toast.state.active).to.be.true;
      expect(toast.state.type).to.equal('error');
      expect(toast.state.message).to.equal('Error updating the event \'ready\'.');
    });

    it('should display info toast with correct message when marking analysis as active', async () => {
      const wrapper = await getMockedWrapper('Ready', mockedData);

      await triggerAction(wrapper, 'Mark Active');

      expect(toast.state.active).to.be.true;
      expect(toast.state.type).to.equal('success');
      expect(toast.state.message).to.equal('Analysis event \'opened\' successful.');
    });

    it('should display info toast with correct message when entering edit mode', async () => {
      const wrapper = getMountedComponent();

      await triggerAction(wrapper, 'Edit');

      expect(toast.state.active).to.be.true;
      expect(toast.state.type).to.equal('success');
      expect(toast.state.message).to.equal('Edit mode has been enabled.');
    });
    it('should display info toast with correct message when exiting edit mode', async () => {
      const wrapper = getMountedComponent();
      await wrapper.setData({edit: true});
      await triggerAction(wrapper, 'Edit');

      expect(toast.state.active).to.be.true;
      expect(toast.state.type).to.equal('info');
      expect(toast.state.message).to.equal('Edit mode has been disabled and changes have not been saved.');
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

  describe('discussions', () => {
    it('Should display a discussion section with three posts', () => {
      const discussionSectionComponent = wrapper.getComponent(DiscussionSection);

      expect(typeof discussionSectionComponent).toBe('object');

      expect(discussionSectionComponent.props('discussions').length).to.equal(3);
    });

    it('Should recieve an new post publish emit and add a new discussion post', async () => {
      const discussionSectionComponent = wrapper.getComponent(DiscussionSection);
      const newPostContent = 'Hello world';

      const discussionFixtureData = fixtureData()['discussions'];

      const newDiscussionPost = {
        post_id: 'e60239a34-h941-44aa-912e-912a993255fe',
        author_id: 'exqkhvidr7uh2ndslsdymbzfbmqjlunk',
        author_fullname: 'Variant Review Report Preparer Person',
        publish_timestamp: '2023-11-01T21:13:22.687000',
        content: newPostContent,
        attachments: [],
        thread: [],
      };

      discussionFixtureData.push(newDiscussionPost);

      postNewDiscussionThreadMock.returns(discussionFixtureData);

      expect(discussionSectionComponent.props('discussions').length).to.equal(3);

      discussionSectionComponent.vm.$emit('discussion:new-post', newPostContent);

      await wrapper.vm.$nextTick();
      await wrapper.vm.$nextTick();

      expect(discussionSectionComponent.props('discussions').length).to.equal(4);
    });

    it('Should receive a delete post emit and remove the discussion post', () => {
      
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
          section: 'Pedigree',
          field: 'Pedigree',
          image_id: '64a2f06a4d4d29b8dc93c2d8',
        };
        attachSectionImageMock.returns(newPedigreeSection);

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
          attachment_field: 'Pedigree',
          content: [{
            type: 'images-dataset',
            field: 'Pedigree',
            value: [{file_id: '635a89aea7b2f21802b74539'}],
          }],
        };
        const analysisWithNewEvidence = fixtureData();
        const pedigreeSectionIndex =
          analysisWithNewEvidence.sections.findIndex((section) => section.header == 'Pedigree');
        analysisWithNewEvidence.sections.splice(pedigreeSectionIndex, 1, imageSection);
        mockedData.returns(analysisWithNewEvidence);
        wrapper = getMountedComponent();
      });

      it('updates section image content with input dialog', async () => {
        updateSectionImageMock.returns({
          section: 'Pedigree',
          field: 'Pedigree',
          image_id: 'different-image-635a89aea7b2f21802b74539',
        });

        const pedigreeSection = wrapper.findComponent('[id=Pedigree]');
        pedigreeSection.vm.$emit('update-image', '635a89aea7b2f21802b74539', 'Pedigree', 'Pedigree');
        await wrapper.vm.$nextTick();

        const fakeImageForUpdate = {data: 'fakeImage.png'};
        inputDialog.confirmation(fakeImageForUpdate);

        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        const reRenderedPedigreeSection = wrapper.findComponent('[id=Pedigree]');

        expect(updateSectionImageMock.called).to.be.true;
        expect(reRenderedPedigreeSection.props().content[0].value[0].file_id)
            .to.equal('different-image-635a89aea7b2f21802b74539');
      });

      it('notifies user when updating section image content fails', async () => {
        updateSectionImageMock.throws('failure happened');

        const pedigreeSection = wrapper.findComponent('[id=Pedigree]');
        pedigreeSection.vm.$emit('update-image', '635a89aea7b2f21802b74539', 'Pedigree', 'Pedigree');
        await wrapper.vm.$nextTick();

        const fakeImageForUpdate = {data: 'fakeImage.png'};
        inputDialog.confirmation(fakeImageForUpdate);

        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        const reRenderedPedigreeSection = wrapper.findComponent('[id=Pedigree]');

        const failureDialog = wrapper.findComponent(NotificationDialog);
        expect(failureDialog.exists()).to.be.true;

        expect(updateSectionImageMock.called).to.be.true;
        expect(reRenderedPedigreeSection.props('content').length).to.equal(1);
      });

      it('allows user to remove image content with input dialog with confirmation', async () => {
        removeSectionImageMock.resolves();

        const pedigreeSection = wrapper.findComponent('[id=Pedigree]');
        pedigreeSection.vm.$emit('update-image', '635a89aea7b2f21802b74539', 'Pedigree', 'Pedigree');
        await wrapper.vm.$nextTick();

        inputDialog.delete();

        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        const confirmationDialog = wrapper.findComponent(NotificationDialog);
        expect(confirmationDialog.exists()).to.be.true;

        notificationDialog.confirmation();
        await wrapper.vm.$nextTick();

        // Neccesary to process several ticks to re-render the section
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        const reRenderedPedigreeSection = wrapper.findComponent('[id=Pedigree]');

        expect(removeSectionImageMock.called).to.be.true;
        expect(reRenderedPedigreeSection.props('content')[0].value.length).to.equal(0);
      });

      it('notifies the user when the image content fails to be removed', async () => {
        removeSectionImageMock.throws('sad-it-did not remove');

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

    describe('when a section has a field that allows supporting evidence to be attached.', () => {
      it('attaches supporting evidence to a field in the section', async () => {
        const newAttachmentData = {
          name: 'fake-attachment-evidence-name',
          data: 'http://sites.uab.edu/cgds',
          attachment_id: 'new-failure-id',
          type: 'link',
          comments: '',
        };

        mockedAttachSectionSupportingEvidence.returns({
          header: 'Mus_musculus (Mouse) Model System',
          field: 'Veterinary Pathology Imaging',
          updated_row: {
            type: 'section-supporting-evidence',
            field: 'Veterinary Pathology Imaging',
            value: [{
              ...newAttachmentData,
              attachment_id: 'new-failure-id',
            }],
          },
        });

        const mouseSection = wrapper.getComponent('[id=Mus_musculus (Mouse) Model System]');

        const mouseFieldToUpdate = mouseSection.props('content').find((row) => {
          return row.field == 'Veterinary Pathology Imaging';
        });

        expect(mouseFieldToUpdate.value.length).to.equal(0);

        mouseSection.vm.$emit('update:content-row', {
          type: 'supporting-evidence',
          operation: 'attach',
          header: 'Mus musculus (Mouse) Model System',
          field: 'Veterinary Pathology Imaging',
          value: {},
        });
        await wrapper.vm.$nextTick();

        inputDialog.confirmation(newAttachmentData);

        // Needs to cycle through updating the prop in the view and then another
        // tick for vuejs to reactively update the supplemental component
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        const updatedMouseSection = wrapper.getComponent('[id=Mus_musculus (Mouse) Model System]');
        const mouseFieldUpdated = updatedMouseSection.props('content').find((row) => {
          return row.field == 'Veterinary Pathology Imaging';
        });
        expect(mouseFieldUpdated.value.length).to.equal(1);
      });

      it('removes the supporting evidence', async () => {
        mockedRemoveSectionSupportingEvidenceFile.resolves({
          header: 'Mus_musculus (Mouse) Model System',
          field: 'Veterinary Histology Report',
        });

        const mouseSection = wrapper.getComponent('[id=Mus_musculus (Mouse) Model System]');
        const mouseFieldToUpdate = mouseSection.props('content').find((row) => {
          return row.field == 'Veterinary Histology Report';
        });
        expect(mouseFieldToUpdate.value.length).to.equal(1);

        mouseSection.vm.$emit('update:content-row', {
          type: 'supporting-evidence',
          operation: 'delete',
          header: 'Mus musculus (Mouse) Model System',
          field: 'Veterinary Histology Report',
          value: {
            type: 'file',
            attachment_id: 'FJKLJFKLDJSKLFDS',
          },
        });
        await wrapper.vm.$nextTick();

        notificationDialog.confirmation();
        await wrapper.vm.$nextTick();

        // Neccesary to process several ticks to re-render the section
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        const updatedMouseSection = wrapper.getComponent('[id=Mus_musculus (Mouse) Model System]');
        const mouseFieldUpdated = updatedMouseSection.props('content').find((row) => {
          return row.field == 'Veterinary Histology Report';
        });
        expect(mouseFieldUpdated.value.length).to.equal(0);
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
            type: 'section-text',
            field: 'Nominated',
            value: [
              'Dr. Person Two (Local) - working with Dr. Person Three in Person Four Lab',
            ],
          },
          {
            type: 'section-text',
            field: 'Reason',
            value: [
              'Contribute a dominant negative patient-variant model to the existing zebrafish model (LOF; in-progress)',
              'Will be used in NBL 240: a research-based undergraduate course at UAB',
            ],
          },
          {
            type: 'section-text',
            field: 'Desired Outcomes',
            value: ['Functional impact confirmation (animal/cell modeling)'],
          },
        ],
      },
      {
        header: 'Medical Summary',
        content: [
          {
            type: 'section-text',
            field: 'Clinical Diagnosis',
            value: ['LMNA-related congenital muscular dystropy'],
          },
          {
            type: 'section-text',
            field: 'Affected Individuals Identified',
            value: ['Male, YOB: 2019'],
          },
        ],
      },
      {
        header: 'Mus musculus (Mouse) Model System',
        content: [
          {
            'type': 'section-text',
            'field': 'Mutation',
            'value': [
              'NF1 c.2970-2972del (p.Met992del)',
            ],
          },
          {
            'type': 'section-text',
            'field': 'Pathogenicity Test',
            'value': [

            ],
          },
          {
            'type': 'section-supporting-evidence',
            'field': 'Veterinary Histology Report',
            'value': [{
              'name': 'CPAM0046-NM_170707.3 (LMNA)_ c.745C_T (p.R249W) other 2.PDF',
              'attachment_id': '64dbcfa43d243bf1e782499f',
              'type': 'file',
              'comments': '  ',
            }],
          },
          {
            'type': 'section-supporting-evidence',
            'field': 'Veterinary Pathology Imaging',
            'value': [],
          },
        ],
      },
      {
        header: 'Pedigree',
        attachment_field: 'Pedigree',
        content: [{
          type: 'images-dataset',
          field: 'Pedigree',
          value: [],
        }],
      },
      {
        header: 'Case Information',
        content: [
          {
            type: 'section-text',
            field: 'Systems',
            value: [
              'Growth Parameters; Craniofacial; Musculoskeletal; Gastrointestinal; Behavior, Cognition;',
            ],
          },
          {
            type: 'section-text',
            field: 'HPO Terms',
            value: [
              'HP:0001508; HP:0001357; HP:0000473; HP:0003560; HP:0003701; HP:0009062; HP:0012389; HP: 0003236;',
            ],
          },
          {
            type: 'section-text',
            field: 'Additional Details',
            value: [
              'Review of VUSes (Why not considered)',
              'NEB (NM_001164508.1)  | c.7385C>G (p.A2462G) (Pat.) and c.16625A>G (p.H5542R) (Mat.). ',
              'LYZL6 (NM_020426.2)  | c.228G>C (p.Q76H) (Mat./Pat.) - Lysozyme Like 6. - No currently known disease',
              'NOL6 (NM_022917.4)  | c.518G>A (p.R173Q) (Pat.) and c.91G>A (p.G31R) (Mat.). - Nucleolar protein 6. -',
            ],
          },
          {
            type: 'section-text',
            field: 'Experimental Design',
            value: [],
          },
          {
            type: 'section-text',
            field: 'Prior Testing',
            value: ['WES - February  2020;'],
          },
        ],
      },
    ],
    discussions: [
      {
        'post_id': '9027ec8d-6298-4afb-add5-6ef710eb5e98',
        'author_id': '3bghhsmnyqi6uxovazy07ryn9q1tqbnt',
        'author_fullname': 'Developer Person',
        'publish_timestamp': '2023-10-09T21:13:22.687000',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
        'attachments': [],
        'thread': [],
      },
      {
        'post_id': 'a677bb36-acf8-4ff9-a406-b113a7952f7e',
        'author_id': 'kw0g790fdx715xsr1ead2jk0pqubtlyz',
        'author_fullname': 'Researcher Person',
        'publish_timestamp': '2023-10-10T21:13:22.687000',
        'content': 'Mauris at mauris eu neque varius suscipit.',
        'attachments': [],
        'thread': [],
      },
      {
        'post_id': 'e6023fa7-b598-416a-9f42-862c826255ef',
        'author_id': 'exqkhvidr7uh2ndslsdymbzfbmqjlunk',
        'author_fullname': 'Variant Review Report Preparer Person',
        'publish_timestamp': '2023-10-13T21:13:22.687000',
        'content': 'Mauris at mauris eu neque varius suscipit.',
        'attachments': [],
        'thread': [],
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
