import {expect, describe, it, afterEach, beforeEach, vi, beforeAll, afterAll} from 'vitest';
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
import {useRouter} from 'vue-router';
import {analysisStore} from '@/stores/analysisStore.js';

vi.mock(import('vue-router'), async (importOriginal) => {
  const mod = await importOriginal();
  return {
    ...mod,
    useRoute: vi.fn(),
    useRouter: vi.fn(() => ({
      push: () => { },
    })),
  };
});

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
      await action.operation();
      break;
    }
  }
}

/**
 * Helper sets up a mocked wrapper with the given latest status and returns it
 * @param {Object} wrapper VueJS component to update the latest status for
 * @param {string} latestStatus The latest status string value
 * @return {Promise<VueWrapper>} A promise that resolves with the mocked Vue wrapper
 */
function updateAnalysisStoreLatestStatus(wrapper, latestStatus) {
  const analysisData = fixtureData();
  analysisData.latest_status = latestStatus;
  analysisStore.forceUpdate(analysisData);
  return wrapper;
}

describe('AnalysisView', () => {
  let mockedData;

  let wrapper;
  let sandbox;

  let mockVueRouterPush;

  let mockAnalysisEventPush;

  let attachSectionImageMock;
  let updateSectionImageMock;
  let removeSectionAttachmentMock;
  let attachSectionAttachmentMock;

  let attachAttachmentMock;
  let removeAttachmentMock;

  let postNewDiscussionThreadMock;
  let deleteDiscussionThreadByIdMock;
  let editDiscussionThreadByIdMock;

  let mockedAttachThirdPartyLink;
  let updateAnalysisSectionsMock;

  beforeAll(() => {
    sandbox = sinon.createSandbox();
    mockedData = sandbox.stub(Analyses, 'getAnalysis').resolves(fixtureData());

    authStore.hasWritePermissions = sandbox.fake.returns(true);

    mockVueRouterPush = sandbox.fake.returns(true);
    useRouter.mockImplementation(() => {
      return {
        push: () => {
          mockVueRouterPush();
        },
      };
    });

    mockAnalysisEventPush = sandbox.stub(Analyses, 'pushAnalysisEvent');

    attachSectionImageMock = sandbox.stub(Analyses, 'attachSectionImage');
    updateSectionImageMock = sandbox.stub(Analyses, 'updateSectionImage');
    removeSectionAttachmentMock = sandbox.stub(Analyses, 'removeSectionAttachment');
    attachSectionAttachmentMock = sandbox.stub(Analyses, 'attachSectionSupportingEvidence');

    attachAttachmentMock = sandbox.stub(Analyses, 'attachSupportingEvidence');
    removeAttachmentMock = sandbox.stub(Analyses, 'removeSupportingEvidence');

    mockedAttachThirdPartyLink = sandbox.stub(Analyses, 'attachThirdPartyLink');

    updateAnalysisSectionsMock = sandbox.stub(Analyses, 'updateAnalysisSections');

    postNewDiscussionThreadMock = sandbox.stub(Analyses, 'postNewDiscussionThread');
    deleteDiscussionThreadByIdMock = sandbox.stub(Analyses, 'deleteDiscussionThreadById');
    editDiscussionThreadByIdMock = sandbox.stub(Analyses, 'editDiscussionThreadById');

    wrapper = getMountedComponent();
  });

  beforeEach(() => {
    mockedData.resolves(fixtureData());
  });

  afterEach(() => {
    sandbox.reset();
  });

  afterAll(() => {
    sandbox.restore();
  });

  describe('when the view renders', () => {
    it('contains the expected content body element', () => {
      const appContent = wrapper.find('app-content');
      expect(appContent.exists()).to.be.true;
    });

    it('contains a header element', () => {
      const appHeader = wrapper.find('app-header');
      expect(appHeader.exists()).to.be.true;
    });

    it('allows user logout', () => {
      const headerComponent = wrapper.getComponent('[data-test=analysis-view-header]');
      headerComponent.vm.$emit('logout');
      expect(mockVueRouterPush.called).to.be.true;
    });

    it('should have a copy button and show a toast with the copied content within it', () => {
      const geneBox = wrapper.getComponent(GeneBox);

      geneBox.vm.$emit('clipboard-copy', 'NM_001017980.3:c.164G>T');

      expect(toast.state.active).to.be.true;
      expect(toast.state.type).to.equal('success');
      expect(toast.state.message).to.equal('Copied NM_001017980.3:c.164G>T to clipboard!');
    });
  });

  describe('the header', () => {
    it('provides the expected headings of sections to be used as anchors', () => {
      const headerComponent = wrapper.get('[data-test="analysis-view-header"]');
      expect(headerComponent.attributes('sectionanchors')).to.equal(
          'Brief,Medical Summary,Mus musculus (Mouse) Model System,Pedigree,' +
        'Case Information,Discussion,Supporting Evidence',
      );
    });

    it('should mark an analysis as ready', async () => {
      wrapper = await updateAnalysisStoreLatestStatus(wrapper, 'Preparation');

      triggerAction(wrapper, 'Mark Ready');

      expect(mockAnalysisEventPush.called).to.be.true;
    });

    it('should display success toast with correct message when marking analysis as ready', async () => {
      wrapper = await updateAnalysisStoreLatestStatus(wrapper, 'Preparation');

      triggerAction(wrapper, 'Mark Ready');

      expect(toast.state.active).to.be.true;
      expect(toast.state.type).to.equal('success');
      expect(toast.state.message).to.equal('Analysis event \'ready\' successful.');
    });

    it('should display error toast with correct message when marking analysis as ready fails', async () => {
      wrapper = await updateAnalysisStoreLatestStatus(wrapper, 'Preparation');
      const error = new Error('Error updating the event \'ready\'.');
      mockAnalysisEventPush.throws(error);

      try {
        await triggerAction(wrapper, 'Mark Ready');
      } catch (error) {
        console.error(error);
      }
      expect(toast.state.active).to.be.true;
      expect(toast.state.type).to.equal('error');
      expect(toast.state.message).to.equal('Error updating the event \'ready\'.');

      mockAnalysisEventPush.reset();
    });

    it('should display info toast with correct message when marking analysis as active', async () => {
      wrapper = await updateAnalysisStoreLatestStatus(wrapper, 'Ready');

      await triggerAction(wrapper, 'Mark Active');

      expect(toast.state.active).to.be.true;
      expect(toast.state.message).to.equal('Analysis event \'opened\' successful.');
      expect(toast.state.type).to.equal('success');
    });

    it('should display info toast with correct message when entering edit mode', () => {
      triggerAction(wrapper, 'Edit');

      expect(toast.state.active).to.be.true;
      expect(toast.state.type).to.equal('success');
      expect(toast.state.message).to.equal('Edit mode has been enabled.');

      // This is done to reset the component to the non-editing state after testing.
      triggerAction(wrapper, 'Edit');
    });

    it('should display info toast with correct message when exiting edit mode', () => {
      // Places the Initial wrapper into the 'Edit' mode
      triggerAction(wrapper, 'Edit');

      // Disabling the 'edit mode and notifying edits haven't been made
      triggerAction(wrapper, 'Edit');

      expect(toast.state.active).to.be.true;
      expect(toast.state.type).to.equal('info');
      expect(toast.state.message).to.equal('Edit mode has been disabled and changes have not been saved.');
    });
  });

  describe('third party links', () => {
    it('should render the input dialog when the attach monday link menu action is clicked', () => {
      const headerComponent = wrapper.getComponent('[data-test=analysis-view-header]');
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

      analysisStore.forceUpdate(fixtureData({['monday_com']: 'https://monday.com'}));

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

    it('should render the input dialog when the attach phenotips link menu action is clicked', () => {
      const headerComponent = wrapper.getComponent('[data-test=analysis-view-header]');
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
      analysisStore.forceUpdate(fixtureData({['phenotips_com']: 'https://phenotips.com'}));
      const headerComponent = wrapper.getComponent('[data-test=analysis-view-header]');
      const actionsProps = headerComponent.props('actions');

      for (const action of actionsProps) {
        if (action.text === 'Connect PhenoTips') {
          action.operation();
        }
      }

      const newAttachmentData = {
        data: 'https://phenotips.com',
        type: 'link',
      };
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

    it('Should receive a discussion:delete-post emit and remove the discussion post', async () => {
      const discussionSectionComponent = wrapper.getComponent(DiscussionSection);

      const deletePostId = '9027ec8d-6298-4afb-add5-6ef710eb5e98';

      const discussionFixtureData = fixtureData()['discussions'].filter((post) => post.post_id != deletePostId);

      deleteDiscussionThreadByIdMock.returns(discussionFixtureData);

      discussionSectionComponent.vm.$emit('discussion:delete-post', deletePostId);

      notificationDialog.confirmation();

      await wrapper.vm.$nextTick();
      await wrapper.vm.$nextTick();
      await wrapper.vm.$nextTick();

      expect(discussionSectionComponent.props('discussions').length).toBe(2);
    });

    it('Should receive a discussion:edit-post emit and work to edit the selected post with new content', async () => {
      const discussionSectionComponent = wrapper.getComponent(DiscussionSection);

      const editPostId = '9027ec8d-6298-4afb-add5-6ef710eb5e98';
      const editPostContent = 'Well my mind is changed, Gundam Wing is the best anime!';

      const discussionFixtureData = fixtureData()['discussions'];
      const postIndex = discussionFixtureData.findIndex((post) => post.post_id == editPostId);

      discussionFixtureData[postIndex].content = editPostContent;

      editDiscussionThreadByIdMock.returns(discussionFixtureData);

      discussionSectionComponent.vm.$emit('discussion:edit-post', editPostId, editPostContent);

      await wrapper.vm.$nextTick();
      await wrapper.vm.$nextTick();

      const updatedPosts = discussionSectionComponent.props('discussions');
      const updatedPostIndex = updatedPosts.findIndex((post) => post.post_id == editPostId);

      expect(updatedPosts[updatedPostIndex].content).toBe(editPostContent);
    });
  });

  describe('supporting evidence', () => {
    describe('when adding supporting evidence as an attachment', () => {
      it('displays the attachment modal when the supplemental form list requests dialog', async () => {
        const supplementalComponent =
          wrapper.getComponent(SupplementalFormList);
        supplementalComponent.vm.$emit('open-modal');

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
        analysisWithNewEvidence.supporting_evidence_files.push(newAttachmentData);
        attachAttachmentMock.returns(analysisWithNewEvidence.supporting_evidence_files);

        const supplementalComponent = wrapper.getComponent(SupplementalFormList);
        expect(supplementalComponent.props('attachments').length).to.equal(1);

        supplementalComponent.vm.$emit('open-modal');

        inputDialog.confirmation(newAttachmentData);

        // Needs to cycle through updating the prop in the view and then another
        // tick for vuejs to reactively update the supplemental component
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();
        expect(supplementalComponent.props('attachments').length).to.equal(2);
      });
    });

    describe('when removing supporting evidence', async () => {
      beforeEach(() => {
        analysisStore.forceUpdate(fixtureData());
      });
      it('prompts a confirmation when an attachment is to be deleted', async () => {
        const supplementalComponent = wrapper.getComponent(SupplementalFormList);
        expect(supplementalComponent.props('attachments').length).to.equal(1);

        const fakeAttachment = {name: 'fake.txt'};
        supplementalComponent.vm.$emit('delete', fakeAttachment);

        const confirmationDialog = wrapper.findComponent(NotificationDialog);
        expect(confirmationDialog.exists()).to.be.true;
      });

      it('can cancel deleting the attachment via the confirmation and not delete the attachment', async () => {
        const fakeAttachment = {name: 'fake.txt'};
        const supplementalComponent = wrapper.getComponent(SupplementalFormList);
        expect(supplementalComponent.props('attachments').length).to.equal(1);

        supplementalComponent.vm.$emit('delete', fakeAttachment);
        notificationDialog.cancel();

        expect(supplementalComponent.props('attachments').length).to.equal(1);
      });

      it('should confirmation to remove the supporting evidence from the analysis', async () => {
        const fakeAttachment = {name: 'fake.txt'};
        const supplementalComponent = wrapper.getComponent(SupplementalFormList);

        expect(supplementalComponent.props('attachments').length).to.equal(1);

        supplementalComponent.vm.$emit('delete', fakeAttachment);

        notificationDialog.confirmation();
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        expect(supplementalComponent.props('attachments').length).to.equal(0);
        expect(removeAttachmentMock.called).to.be.true;
      });

      it('should alert user when fails to delete', async () => {
        removeAttachmentMock.throws('Failed to delete');

        const fakeAttachment = {name: 'fake.txt'};
        const supplementalComponent = wrapper.getComponent(SupplementalFormList);

        expect(supplementalComponent.props('attachments').length).to.equal(1);

        supplementalComponent.vm.$emit('delete', fakeAttachment);

        notificationDialog.confirmation();
        await wrapper.vm.$nextTick();

        expect(supplementalComponent.props('attachments').length).to.equal(1);
        expect(removeAttachmentMock.called).to.be.true;
      });
    });
  });

  describe('sections', () => {
    describe('when an image section does not have an image', () => {
      it('accepts an image render as content', async () => {
        const updatedSectionField= {
          type: 'images-dataset',
          field: 'Pedigree',
          value: [{file_id: '64a2f06a4d4d29b8dc93c2d8'}],
        };
        attachSectionImageMock.returns(updatedSectionField);

        const pedigreeSection = wrapper.findComponent('[id=Pedigree]');
        pedigreeSection.vm.$emit('attach-image', 'Pedigree');

        const fakeImage = {data: 'fakeImage.png'};
        inputDialog.confirmation(fakeImage);

        const reRenderedPedigreeSection = wrapper.findComponent('[id=Pedigree]');

        expect(reRenderedPedigreeSection.props('content').length).to.equal(1);
      });
    });

    describe('when an image section has an image in it', () => {
      beforeEach(() => {
        const imageFieldValue = {file_id: '635a89aea7b2f21802b74539'};
        const analysisWithNewEvidence = fixtureData();
        analysisWithNewEvidence.sections = addSectionFieldValue('Pedigree', 'Pedigree', imageFieldValue);
        analysisStore.forceUpdate(analysisWithNewEvidence);
      });

      // INVESTIGATE ANGELINA
      it.skip('updates section image content with input dialog', async () => {
        updateSectionImageMock.returns({
          section: 'Pedigree',
          field: 'Pedigree',
          image_id: 'different-image-635a89aea7b2f21802b74539',
        });

        const pedigreeSection = wrapper.findComponent('[id=Pedigree]');
        pedigreeSection.vm.$emit('update-image', '635a89aea7b2f21802b74539', 'Pedigree', 'Pedigree');

        const fakeImageForUpdate = {data: 'fakeImage.png'};
        inputDialog.confirmation(fakeImageForUpdate);

        const reRenderedPedigreeSection = wrapper.findComponent('[id=Pedigree]');
        expect(updateSectionImageMock.called).to.be.true;
        expect(reRenderedPedigreeSection.props().content[0].value[0].file_id)
            .to.equal('different-image-635a89aea7b2f21802b74539');
      });

      it('notifies user when updating section image content fails', async () => {
        updateSectionImageMock.throws('failure happened');

        const pedigreeSection = wrapper.findComponent('[id=Pedigree]');
        pedigreeSection.vm.$emit('update-image', '635a89aea7b2f21802b74539', 'Pedigree', 'Pedigree');

        const fakeImageForUpdate = {data: 'fakeImage.png'};
        inputDialog.confirmation(fakeImageForUpdate);

        await wrapper.vm.$nextTick();

        const reRenderedPedigreeSection = wrapper.findComponent('[id=Pedigree]');

        const failureDialog = wrapper.findComponent(NotificationDialog);
        expect(failureDialog.exists()).to.be.true;

        expect(updateSectionImageMock.called).to.be.true;
        expect(reRenderedPedigreeSection.props('content').length).to.equal(1);
      });

      it('allows user to remove section image with input dialog confirmation', async () => {
        const sectionName = 'Pedigree';
        const fieldName = 'Pedigree';
        removeSectionAttachmentMock.resolves(removeFieldValue('Pedigree', 'Pedigree'));

        const pedigreeSection = wrapper.findComponent(`[id=${sectionName}]`);
        pedigreeSection.vm.$emit('update-image', '635a89aea7b2f21802b74539', sectionName, fieldName);

        inputDialog.delete();

        await wrapper.vm.$nextTick();

        const confirmationDialog = wrapper.findComponent(NotificationDialog);
        expect(confirmationDialog.exists()).to.be.true;

        notificationDialog.confirmation();

        // Neccesary to process several ticks to re-render the section
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        const reRenderedPedigreeSection = wrapper.findComponent('[id=Pedigree]');

        expect(removeSectionAttachmentMock.called).to.be.true;
        expect(reRenderedPedigreeSection.props('content')[0].value.length).to.equal(0);
      });

      it('notifies the user when the image content fails to be removed', async () => {
        removeSectionAttachmentMock.throws('sad-it-did not remove');

        const pedigreeSection = wrapper.findComponent('[id=Pedigree]');
        pedigreeSection.vm.$emit('update-image', 'Pedigree');

        inputDialog.delete();

        notificationDialog.confirmation();

        const failureNotificationDialog = wrapper.findComponent(NotificationDialog);
        expect(failureNotificationDialog.exists()).to.be.true;
      });
    });

    describe('when a section has a field that allows attachments', () => {
      it('may attach a link to that field', async () => {
        const sectionName = 'Mus musculus (Mouse) Model System';
        const sectionId = 'Mus_musculus (Mouse) Model System';
        const fieldName = 'Veterinary Pathology Imaging';
        const newAttachmentData = {
          name: 'fake-attachment-evidence-name',
          data: 'http://sites.uab.edu/cgds',
          attachment_id: 'new-failure-id',
          type: 'link',
          comments: '',
        };

        attachSectionAttachmentMock.returns(addFieldValue(sectionName, fieldName, newAttachmentData));

        const mouseSection = wrapper.getComponent(`[id=${sectionId}]`);
        const mouseFieldToUpdate = mouseSection.props('content').find((row) => {
          return row.field == fieldName;
        });

        expect(mouseFieldToUpdate.value.length).to.equal(0);

        mouseSection.vm.$emit('update:content-row', {
          type: 'supporting-evidence',
          operation: 'attach',
          header: sectionName,
          field: fieldName,
          value: {},
        });

        inputDialog.confirmation(newAttachmentData);

        // Needs to cycle through updating the prop in the view and then another
        // tick for vuejs to reactively update the supplemental component
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        const updatedMouseSection = wrapper.getComponent(`[id=${sectionId}]`);
        const mouseFieldUpdated = updatedMouseSection.props('content').find((row) => {
          return row.field == fieldName;
        });
        expect(mouseFieldUpdated.value.length).to.equal(1);
      });

      it('removes the supporting evidence from field', async () => {
        const sectionId = 'Mus_musculus (Mouse) Model System';
        const sectionName = 'Mus musculus (Mouse) Model System';
        const fieldName = 'Veterinary Histology Report';

        removeSectionAttachmentMock.resolves(removeFieldValue(sectionName, fieldName));

        const mouseSection = wrapper.getComponent(`[id=${sectionId}]`);
        const mouseFieldToUpdate = mouseSection.props('content').find((row) => {
          return row.field == fieldName;
        });
        expect(mouseFieldToUpdate.value.length).to.equal(1);

        mouseSection.vm.$emit('update:content-row', {
          type: 'supporting-evidence',
          operation: 'delete',
          header: sectionName,
          field: fieldName,
          value: {
            type: 'file',
            attachment_id: 'FJKLJFKLDJSKLFDS',
          },
        });

        notificationDialog.confirmation();

        // Neccesary to process several ticks to re-render the section
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        const updatedMouseSection = wrapper.getComponent(`[id=${sectionId}]`);
        const mouseFieldUpdated = updatedMouseSection.props('content').find((row) => {
          return row.field == fieldName;
        });
        expect(mouseFieldUpdated.value.length).to.equal(0);
      });
    });
  });

  describe('Saving and canceling analysis changes displays toasts', () => {
    beforeEach(() => {
      updateAnalysisSectionsMock.resolves([]);
    });

    it('should display success toast when saving analysis changes', async () => {
      await triggerAction(wrapper, 'Edit');

      const saveModal = wrapper.findComponent(SaveModal);

      saveModal.vm.$emit('save');
      await wrapper.vm.$nextTick();
      await wrapper.vm.$nextTick();

      expect(toast.state.active).to.be.true;
      expect(toast.state.type).to.equal('success');
      expect(toast.state.message).to.equal('Analysis updated successfully.');
    });
  });
});


/**
 * A list of sections from the test fixture data that includes the added field value
 * @param {string} sectionName of the section to add the value to
 * @param {string} fieldName of the field to add the value to
 * @param {Object} value the value to insert into the values for that field and section
 * @return {Array} list of Section objects
 */
function addSectionFieldValue(sectionName, fieldName, value) {
  const sections = fixtureData().sections;
  const field = sections.find((section) => {
    return section.header == sectionName;
  })?.content.find((row) => {
    return row.field == fieldName;
  });

  if (!field) {
    return {};
  }

  field.value.push(value);
  return sections;
}

/**
 * Adds teh value to the field within a section from the test fixture data, if no field is found within the section,
 * an empty object is returned.
 * @param {string} sectionName of the section to add the value to
 * @param {string} fieldName of the field to add the value to
 * @param {Object} value the value to insert into the values for that field and section
 * @return {Array} field with the added field content
 */
function addFieldValue(sectionName, fieldName, value) {
  const sections = fixtureData().sections;
  const field = sections.find((section) => {
    return section.header == sectionName;
  })?.content.find((row) => {
    return row.field == fieldName;
  });

  if (!field) {
    return {};
  }

  field.value.push(value);
  return field;
}

/**
 * Removes the values of the field within a section, if no field is found within the section, an empty object is
 * returned.
 * @param {string} sectionName of the section to add the value to
 * @param {string} fieldName of the field remove the value
 * @param {Object} value the value to insert into the values for that field and section
 * @return {Object} field from within section
 */
function removeFieldValue(sectionName, fieldName) {
  const sections = fixtureData().sections;
  const field = sections.find((section) => {
    return section.header == sectionName;
  })?.content.find((row) => {
    return row.field == fieldName;
  });

  if (!field) {
    return {};
  }

  field.value = [];

  return field;
}

/**
 * Returns fixture data
 *
 * @param {Object} attributes from the analysis to override
 * @return {Object} containing analysis data for CPAM0046.
 */
function fixtureData(attributes) {
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
    ...attributes,
  };
}
