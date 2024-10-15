<template>
  <div>
    <app-header>
      <AnalysisViewHeader
        :actions="menuActions"
        :titleText="analysisName"
        :sectionAnchors="sectionsHeaders"
        :username="authStore.getUsername()"
        :workflow_status="latestStatus"
        @logout="onLogout"
        :third_party_links="thirdPartyLinks"
        data-test="analysis-view-header"
      >
      </AnalysisViewHeader>
      <Toast data-test="toast" />
    </app-header>
    <app-content>
      <GeneBox
        v-for="genomicUnit in genomicUnitsList"
        :key="genomicUnit.id"
        :name="analysisName"
        :gene="genomicUnit.gene"
        :transcripts="genomicUnit.transcripts"
        :variants="genomicUnit.variants"
        @clipboard-copy="copyToClipboard"
      />
      <SectionBox
        v-for="(section) in sectionsList"
        :id="section.header.replace(' ', '_')"
        :key="`${section.header}`"
        :analysis_name="analysisName"
        :header="section.header"
        :content="section.content"
        :attachmentField="section.attachment_field"
        :writePermissions="authStore.hasWritePermissions()"
        :edit="edit"
        @attach-image="attachSectionImage"
        @update-image="updateSectionImage"
        @update:content-row="onAnalysisContentUpdated"
        @download="downloadSupportingEvidence"
      />
      <DiscussionSection
        id="Discussion"
        :discussions="discussions"
        :userClientId="authStore.getClientId()"
        :actions="discussionContextActions"
        @discussion:new-post="addDiscussionPost"
        @discussion:edit-post="editDiscussionPost"
        @discussion:delete-post="deleteDiscussionPost"
      />
      <SupplementalFormList
        id="Supporting_Evidence"
        :attachments="attachments"
        :writePermissions="authStore.hasWritePermissions()"
        @open-modal="addSupportingEvidence"
        @delete="removeSupportingEvidence"
        @edit="editSupportingEvidence"
        @download="downloadSupportingEvidence"
      />
      <InputDialog />
      <NotificationDialog data-test="notification-dialog" />
      <SaveModal
        class="save-modal"
        v-if="edit"
        @canceledit="cancelAnalysisChanges"
        @save="saveAnalysisChanges"
      />
    </app-content>
  </div>
</template>

<script setup>
import {onMounted, ref, computed} from 'vue';

import Analyses from '@/models/analyses.js';
import AnalysisViewHeader from '@/components/AnalysisView/AnalysisViewHeader.vue';
import SectionBox from '@/components/AnalysisView/SectionBox.vue';
import GeneBox from '@/components/AnalysisView/GeneBox.vue';
import InputDialog from '@/components/Dialogs/InputDialog.vue';
import NotificationDialog from '@/components/Dialogs/NotificationDialog.vue';
import Toast from '@/components/Dialogs/Toast.vue';
import SupplementalFormList from '@/components/AnalysisView/SupplementalFormList.vue';
import SaveModal from '@/components/AnalysisView/SaveModal.vue';
import DiscussionSection from '../components/AnalysisView/DiscussionSection.vue';

import inputDialog from '@/inputDialog.js';
import notificationDialog from '@/notificationDialog.js';
import toast from '@/toast.js';

import {authStore} from '@/stores/authStore.js';
import {analysisStore} from '@/stores/analysisStore.js';
import {StatusType} from '@/config.js';
import {useRouter} from 'vue-router';

const router = useRouter();

const props = defineProps({
  analysis_name: {
    type: String,
    default: '',
  },
});

const edit = ref(false);

const analysisName = computed(() => {
  return analysisStore.analysis.name;
});

const latestStatus = computed(() => {
  return analysisStore.analysis.latest_status;
});

const thirdPartyLinks = computed(() => {
  return analysisStore.analysis.third_party_links;
});

const sectionsHeaders = computed(() => {
  const sections = analysisStore.analysis.sections.map((section) => {
    return section.header;
  });
  sections.push('Discussion');
  sections.push('Supporting Evidence');
  return sections;
});

const menuActions = computed(() => {
  const actionChoices = [];
  actionChoices.push({
    icon: 'paperclip',
    text: 'Attach',
    operation: addSupportingEvidence,
  });

  if ( authStore.hasWritePermissions() ) {
    return actionChoices;
  }

  const prependingActions = [];
  prependingActions.push({
    icon: 'pencil',
    text: 'Edit',
    operation: () => {
      if (!edit.value) {
        toast.success('Edit mode has been enabled.');
      } else {
        toast.info('Edit mode has been disabled and changes have not been saved.');
      }
      edit.value = !edit.value;
    },
  });

  if (analysisStore.analysis.latest_status === 'Preparation') {
    prependingActions.push({
      icon: StatusType['Ready'].icon,
      text: 'Mark Ready',
      operation: () => {
        pushAnalysisEvent(Analyses.EventType.READY);
      },
    });
  } else if (analysisStore.analysis.latest_status === 'Ready') {
    prependingActions.push({
      icon: StatusType['Active'].icon,
      text: 'Mark Active',
      operation: () => {
        pushAnalysisEvent(Analyses.EventType.OPEN);
      },
    });
  } else {
    prependingActions.push({
      icon: StatusType['Approved'].icon,
      text: 'Approve',
      operation: () => {
        pushAnalysisEvent(Analyses.EventType.APPROVE);
      },
    }, {
      icon: StatusType['On-Hold'].icon,
      text: 'Hold',
      operation: () => {
        pushAnalysisEvent(Analyses.EventType.HOLD);
      },
    }, {
      icon: StatusType['Declined'].icon,
      text: 'Decline',
      operation: () => {
        pushAnalysisEvent(Analyses.EventType.DECLINE);
      },
    });
  }
  prependingActions.push({divider: true});
  actionChoices.unshift(...prependingActions);

  actionChoices.push({
    text: 'Attach Monday.com',
    operation: addMondayLink,
  });

  actionChoices.push({
    text: 'Connect PhenoTips',
    operation: addPhenotipsLink,
  });

  return actionChoices;
});

const discussionContextActions = computed(() => {
  return [
    {
      icon: 'pencil',
      text: 'Edit',
      emit: 'edit',
      operation: () => {},
    },
    {
      icon: 'xmark',
      text: 'Delete',
      emit: 'delete',
      operation: () => {},
    },
  ];
});

const sectionsList = computed(() => {
  return analysisStore.analysis.sections;
});

const attachments = computed(() => {
  return analysisStore.analysis.supporting_evidence_files;
});

const discussions = computed(() => {
  return analysisStore.analysis.discussions;
});

const genomicUnitsList = computed(() => {
  return analysisStore.analysis.genomic_units;
});

/**
 * Handles updates to analysis content when a content row is modified. If the content type is 'supporting-evidence'
 * triggers an attachment change instead.
 *
 * @param {Object} contentRow - The row of content being updated.
 */
function onAnalysisContentUpdated(contentRow) {
  if (typeof(contentRow.type) !== 'undefined' && 'supporting-evidence' === contentRow.type ) {
    fieldSectionAttachmentChanged(contentRow);
    return;
  }

  if (!(contentRow.header in analysisStore.updatedContent)) {
    analysisStore.updatedContent[contentRow.header] = {};
  }

  analysisStore.updatedContent[contentRow.header][contentRow.field] = contentRow.value;
}

/**
 * Saves the changes to the analysis and reloads the page.
 */
async function saveAnalysisChanges() {
  await analysisStore.saveChanges();
  location.reload();
  edit.value = false;
  toast.success('Analysis updated successfully.');
}

/**
 * Cancels the changes made to the analysis and disables edit mode.
 */
function cancelAnalysisChanges() {
  analysisStore.cancelChanges();
  edit.value = false;
  toast.info('Edit mode has been disabled and changes have not been saved.');
}

/**
 * Attaches an image to a specified section and field.
 *
 * @param {string} sectionName - name of the section.
 * @param {string} field - The section's field to attach an image to
 */
async function attachSectionImage(sectionName, field) {
  const includeComments = false;

  const attachment = await inputDialog
      .confirmText('Attach')
      .cancelText('Cancel')
      .file(includeComments, 'file', '.png, .jpg, .jpeg, .bmp')
      .prompt();

  if (!attachment) {
    return;
  }

  try {
    analysisStore.attachSectionImage(sectionName, field, attachment);
  } catch (error) {
    await notificationDialog.title('Failure').confirmText('Ok').alert(error);
  }
}

/**
 * Removes an image from a specified section and field.
 *
 * @param {string} fileId - ID of the file to remove.
 * @param {string} sectionName - name of the section.
 * @param {string} field - The section's field to remove image from
 */
async function removeSectionImage(fileId, sectionName, field) {
  const confirmedDelete = await notificationDialog
      .title(`Remove ${field} attachment`)
      .confirmText('Remove')
      .cancelText('Cancel')
      .confirm(
          'This operation will permanently remove the image. Are you sure you want to remove?',
      );

  if (!confirmedDelete) {
    return;
  }

  try {
    await analysisStore.removeSectionImage(fileId, sectionName, field);
  } catch (error) {
    await notificationDialog.title('Failure').confirmText('Ok').alert(error);
  }
}

/**
 * Updates an image in a specified section and field.
 *
 * @param {string} fileId - The ID of the file to update.
 * @param {string} sectionName - name of the section.
 * @param {string} field - The section's field to update image
 */
async function updateSectionImage(fileId, sectionName, field) {
  const includeComments = false;
  const attachment = await inputDialog
      .confirmText('Update')
      .deleteText('Remove')
      .cancelText('Cancel')
      .file(includeComments, 'file', '.png, .jpg, .jpeg, .bmp')
      .prompt();

  if (!attachment) {
    return;
  }

  if ('DELETE' == attachment) {
    await removeSectionImage(fileId, sectionName, field);
    return;
  }

  try {
    await analysisStore.updateSectionImage(fileId, sectionName, field, attachment);
  } catch (error) {
    await notificationDialog.title('Failure').confirmText('Ok').alert(error);
  }
}

async function addSectionAttachment(section, field, evidence) {
  const includeComments = true;
  const includeName = true;
  const attachment = await inputDialog
      .confirmText('Add')
      .cancelText('Cancel')
      .file(includeComments, 'file', '.pdf, .jpg, .jpeg, .png')
      .url(includeComments, includeName)
      .prompt();

  if (!attachment) {
    return;
  }

  try {
    const updatedSectionField = await Analyses.attachSectionSupportingEvidence(
        analysisName,
        section,
        field,
        attachment,
    );
    const sectionWithReplacedField = analysisStore.replaceFieldInSection(section, updatedSectionField);
    analysisStore.replaceAnalysisSection(sectionWithReplacedField);
  } catch (error) {
    console.error('Updating the analysis did not work');
  }
}
async function removeSectionAttachment(section, field, attachment) {
  const confirmedDelete = await notificationDialog
      .title(`Remove attachment`)
      .confirmText('Delete')
      .cancelText('Cancel')
      .confirm(`Removing '${attachment.name}' from ${field} in ${section}?`);

  if (!confirmedDelete) {
    return;
  }

  try {
    const updatedSectionField =
      await Analyses.removeSectionAttachment(
          analysisStore.analysis.analysis_name, section, field, attachment.attachment_id,
      );
    const sectionWithReplacedField = analysisStore.replaceFieldInSection(section, updatedSectionField);

    analysisStore.replaceAnalysisSection(sectionWithReplacedField);
  } catch (error) {
    await notificationDialog.title('Failure').confirmText('Ok').alert(error);
  }
}

async function fieldSectionAttachmentChanged(contentRow) {
  const operations = {
    'attach': addSectionAttachment,
    'delete': removeSectionAttachment,
  };

  if (!Object.hasOwn(operations, contentRow.operation)) {
    // Warning here that the operation is invalid and move on
    return;
  }

  operations[contentRow.operation](contentRow.header, contentRow.field, contentRow.value);
}

async function addSupportingEvidence() {
  const includeComments = true;
  const includeName = true;
  const attachment = await inputDialog
      .confirmText('Add')
      .cancelText('Cancel')
      .file(includeComments, 'file', '.pdf, .jpg, .jpeg, .png')
      .url(includeComments, includeName)
      .prompt();

  if (!attachment) {
    return;
  }

  try {
    await analysisStore.addAttachment(attachment);
  } catch (error) {
    await notificationDialog.title('Failure').confirmText('Ok').alert(error);
  }
}

async function editSupportingEvidence(attachment) {
  const updatedAttachment = await inputDialog
      .confirmText('Update')
      .cancelText('Cancel')
      .edit(attachment)
      .prompt();

  if (!updatedAttachment) {
    return;
  }

  try {
    analysisStore.updateAttachment(updatedAttachment);
  } catch (error) {
    await notificationDialog.title('Failure').confirmText('Ok').alert(error);
  }
}

async function removeSupportingEvidence(attachmentToDelete) {
  const confirmedDelete = await notificationDialog
      .title('Delete Supporting Information?')
      .confirmText('Delete')
      .cancelText('Cancel')
      .confirm('Deleting this item will remove it from the supporting evidence list.');

  if (!confirmedDelete) {
    return;
  }

  try {
    await analysisStore.removeAttachment(attachmentToDelete);
  } catch (error) {
    await notificationDialog.title('Failure').confirmText('Ok').alert(error);
  }
}

function downloadSupportingEvidence(attachmentToDownload) {
  Analyses.downloadSupportingEvidence(
      attachmentToDownload.attachment_id,
      attachmentToDownload.name,
  );
}

function onLogout() {
  router.push({name: 'logout'});
}

async function addMondayLink() {
  const includeComments = false;
  const includeName = false;
  const mondayLink = await inputDialog
      .confirmText('Add')
      .cancelText('Cancel')
      .url(includeComments, includeName)
      .prompt();

  if (!mondayLink) {
    return;
  }

  try {
    const updatedAnalysis = await Analyses.attachThirdPartyLink(
        analysisName,
        'monday_com',
        mondayLink.data,
    );

    analysisStore.forceUpdate(updatedAnalysis);
  } catch (error) {
    console.error('Updating the analysis did not work', error);
  }
}

async function addPhenotipsLink() {
  const includeComments = false;
  const includeName = false;
  const phenotipsLink = await inputDialog
      .confirmText('Add')
      .cancelText('Cancel')
      .url(includeComments, includeName)
      .prompt();

  if (!phenotipsLink) {
    return;
  }

  try {
    const updatedAnalysis = await Analyses.attachThirdPartyLink(
        analysisName,
        'phenotips_com',
        phenotipsLink.data,
    );

    analysisStore.forceUpdate(updatedAnalysis);
  } catch (error) {
    console.error('Updating the analysis did not work', error);
  }
}

async function pushAnalysisEvent(eventType) {
  try {
    const updatedAnalysis = await Analyses.pushAnalysisEvent(analysisName, eventType);
    analysisStore.forceUpdate(updatedAnalysis);
    toast.success(`Analysis event '${eventType}' successful.`);
  } catch (error) {
    toast.error(`Error updating the event '${eventType}'.`);
  }
}

async function addDiscussionPost(newPostContent) {
  const discussions = await Analyses.postNewDiscussionThread(analysisName, newPostContent);
  analysisStore.analysis.discussions = discussions;
}

async function editDiscussionPost(postId, postContent) {
  const discussions = await Analyses.editDiscussionThreadById(analysisName, postId, postContent);
  analysisStore.analysis.discussions = discussions;
}

async function deleteDiscussionPost(postId) {
  const confirmedDelete = await notificationDialog
      .title(`Remove Discussion Post`)
      .confirmText('Delete')
      .cancelText('Cancel')
      .confirm(`Deleting your discussion post from the section.`);
  if (!confirmedDelete) {
    return;
  }
  try {
    const discussions = await Analyses.deleteDiscussionThreadById(analysisName, postId);
    analysisStore.analysis.discussions = discussions;
  } catch (error) {
    await notificationDialog.title('Failure').confirmText('Ok').alert(error);
  }
}

function copyToClipboard(copiedText) {
  toast.success(`Copied ${copiedText} to clipboard!`);
}

onMounted(async () => {
  await analysisStore.getAnalysis(props.analysis_name);
});
</script>

<style scoped>

app-content {
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

app-header {
  position: sticky;
  top: 0px;
  z-index: 10;
}

.save-modal {
  position: sticky;
  bottom: 0;
}
</style>
