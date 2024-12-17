<template>
    <app-header>
      <AnalysisViewHeader
        :actions="actionChoices"
        :titleText="analysisName"
        :sectionAnchors="sectionsHeaders"
        :username="username"
        :workflow_status="latestStatus"
        @logout="onLogout"
        :third_party_links="thirdPartyLinks"
        data-test="analysis-view-header"
      >
      </AnalysisViewHeader>
      <ToastDialog data-test="toast" ref="rosalution-toast"/>
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
        :writePermissions="hasWritePermissions"
        :edit="edit"
        @attach-image="attachSectionImage"
        @update-image="updateSectionImage"
        @update:content-row="onAnalysisContentUpdated"
        @download="downloadSupportingEvidence"
      />
      <DiscussionSection
        id="Discussion"
        :discussions="discussions"
        :userClientId="clientId"
        :actions="discussionContextActions"
        @discussion:new-post="addDiscussionPost"
        @discussion:edit-post="editDiscussionPost"
        @discussion:delete-post="deleteDiscussionPost"
        @discussion:open-modal="openDiscussionModal"
      />
      <SupplementalFormList
        id="Supporting_Evidence"
        :attachments="attachments"
        :writePermissions="hasWritePermissions"
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
</template>

<script setup>
import {onMounted, ref, computed, watch, useTemplateRef} from 'vue';

import AnalysisViewHeader from '@/components/AnalysisView/AnalysisViewHeader.vue';
import SectionBox from '@/components/AnalysisView/SectionBox.vue';
import GeneBox from '@/components/AnalysisView/GeneBox.vue';
import InputDialog from '@/components/Dialogs/InputDialog.vue';
import NotificationDialog from '@/components/Dialogs/NotificationDialog.vue';
import ToastDialog from '@/components/Dialogs/ToastDialog.vue';
import SupplementalFormList from '@/components/AnalysisView/SupplementalFormList.vue';
import SaveModal from '@/components/AnalysisView/SaveModal.vue';
import DiscussionSection from '@/components/AnalysisView/DiscussionSection.vue';

import inputDialog from '@/inputDialog.js';
import notificationDialog from '@/notificationDialog.js';

import {authStore} from '@/stores/authStore.js';
import {analysisStore} from '@/stores/analysisStore.js';
import {useRouter} from 'vue-router';
import {useActionMenu} from '@/components/AnalysisView/useActionMenu.js';

const router = useRouter();

const props = defineProps({
  analysis_name: {
    type: String,
    default: '',
  },
});

const edit = ref(false);

const toastRef = useTemplateRef('rosalution-toast');
let toast = {};

const analysisName = computed(() => {
  return analysisStore.analysisName();
});

const latestStatus = computed(() => {
  return analysisStore.latestStatus();
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

const username = computed(() => {
  return authStore.getUsername();
});

const clientId = computed(() => {
  return authStore.getClientId();
});

const hasWritePermissions = computed(() => {
  return authStore.hasWritePermissions();
});

const {actionChoices, builder} = useActionMenu();

watch([hasWritePermissions, latestStatus], () => {
  builder.clear();
  if ( !authStore.hasWritePermissions() ) {
    builder.addMenuAction('Attach', 'paperclip', addSupportingEvidence);
    return;
  }

  builder.addMenuAction('Edit', 'pencil', enableEditing);
  builder.addWorkflowActions(latestStatus.value, pushAnalysisEvent);
  builder.addDivider();

  builder.addMenuAction('Attach', 'paperclip', addSupportingEvidence);
  builder.addMenuAction('Attach Monday.com', null, addMondayLink);
  builder.addMenuAction('Connect PhenoTips', null, addPhenotipsLink);
});

const discussionContextActions = [
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
 * Enables the view to support in-line editing of the analysis.
 */
function enableEditing() {
  if (!edit.value) {
    toast.success('Edit mode has been enabled.');
  } else {
    toast.info('Edit mode has been disabled and changes have not been saved.');
  }
  edit.value = !edit.value;
}

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

  analysisStore.addUpdatedContent(contentRow.header, contentRow.field, contentRow.value);
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

/**
 * Adds an attachment to a specified section and field.
 *
 * @param {string} section - The section to which the attachment is added.
 * @param {string} field - The field within the section for the attachment.
 * @param {Object} evidence - The evidence to be attached.
 */
async function addSectionAttachment(section, field, evidence) {
  const includeComments = true;
  const includeName = true;
  const attachment = await inputDialog
      .confirmText('Add')
      .cancelText('Cancel')
      .file(includeComments, 'file', '.pdf, .jpg, .jpeg, .png, .gb')
      .url(includeComments, includeName)
      .prompt();

  if (!attachment) {
    return;
  }

  try {
    await analysisStore.attachSectionAttachment(section, field, attachment);
  } catch (error) {
    console.error(`Updating the analysis did not work. Error: ${error}`);
  }
}

/**
 * Removes the specified attachment from the section and field
 *
 * @param {string} section - The section name to which the attachment is added.
 * @param {string} field - The field name within the section for the attachment.
 * @param {Object} attachment - The attachment to add
 */
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
    await analysisStore.removeSectionAttachment(section, field, attachment.attachment_id);
  } catch (error) {
    await notificationDialog.title('Failure').confirmText('Ok').alert(error);
  }
}

/**
 * Handles changes to section attachments based on the provided operation.
 *
 * @param {Object} contentRow - The content row containing the operation, header, field, and value.
 * @param {string} contentRow.operation - String that indicates the type of operation 'attach' or 'delete'
 * @param {string} contentRow.header - The name of the section the attachment is in
 * @param {string} contentRow.header - The name of the field being operated on within a section
 * @param {Object} contentRow.value - the modified content
 */
async function fieldSectionAttachmentChanged(contentRow) {
  const operations = {
    'attach': addSectionAttachment,
    'delete': removeSectionAttachment,
  };

  if (!Object.hasOwn(operations, contentRow.operation)) {
    console.warning(`${contentRow.operation} is not an available operation for section attachments.`);
    return;
  }

  await operations[contentRow.operation](contentRow.header, contentRow.field, contentRow.value);
}

/**
 * Prompts input dialog to add new attachment to the Analysis.
 */
async function addSupportingEvidence() {
  const includeComments = true;
  const includeName = true;
  const attachment = await inputDialog
      .confirmText('Add')
      .cancelText('Cancel')
      .file(includeComments, 'file', '.pdf, .jpg, .jpeg, .png, .gb')
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

/**
 * Prompts input dialog to modify existing attachment in the Analysis.
 *
 * @param {Object} attachment Attachment to edit
 */
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

/**
 * Prompts input dialog to remove existing attachment in the Analysis.
 *
 * @param {Object} attachmentToDelete to remove
 */
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

/**
 * Downloads an attachment by its ID within the analysis.
 *
 * @param {Object} attachmentToDownload to download
 */
function downloadSupportingEvidence(attachmentToDownload) {
  analysisStore.downloadAttachment(attachmentToDownload);
}

/**
 * Logs user out of Rosalution
 */
function onLogout() {
  router.push({name: 'logout'});
}

/**
 * Attaches Monday 3rd Party linkout for C-PAM Case management
 */
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
    await analysisStore.attachThirdPartyLink('monday_com', mondayLink.data);
  } catch (error) {
    console.error('Updating the analysis did not work', error);
  }
}

/**
 * Attaches Phenotips linkout for C-PAM Case management
 */
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
    await analysisStore.attachThirdPartyLink('phenotips_com', phenotipsLink.data);
  } catch (error) {
    console.error('Updating the analysis did not work', error);
  }
}

/**
 * Updates the Analysis with a new event.
 *
 * @param {string} eventType The type of event to push to Analysis
 */
async function pushAnalysisEvent(eventType) {
  try {
    await analysisStore.pushEvent(eventType);
    toast.success(`Analysis event '${eventType}' successful.`);
  } catch (error) {
    toast.error(`Error updating the event '${eventType}'. Error: ${error}`);
  }
}

/**
 * Adds a new discussion post to the analysis.
 *
 * @param {string} newPostContent - The content of the new discussion post.
 */
async function addDiscussionPost(newPostContent) {
  await analysisStore.addDiscussionPost(newPostContent);
}

/**
 * Edits a discussion post in the analysis.
 *
 * @param {string} postId - The identifier of the post to edit
 * @param {string} postContent - The content of the updated discussion post.
 */
async function editDiscussionPost(postId, postContent) {
  await analysisStore.editDiscussionPost(postId, postContent);
}

/**
 * Prompts to delete a discussion post in the analysis.
 *
 * @param {string} postId - The identifier of the post to delete
 */
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
    await analysisStore.deleteDiscussionPost(postId);
  } catch (error) {
    await notificationDialog.title('Failure').confirmText('Ok').alert(error);
  }
}


/**
 * Prompts to add an attachment to a discussion post in the analysis.
 *
 * @param {string} postId - The identifier of the post to delete
 */
async function openDiscussionModal(postId) {
  console.log('Doing something here');
  const includeComments = false;
  const includeName = true;
  // const defaultComments = 'This attachment is referenced in the Discussion attachment.';
  const attachment = await inputDialog
      .confirmText('Attach')
      .cancelText('Cancel')
      .file(includeComments, 'file', '.png, .jpg, .jpeg, .bmp')
      .url(includeComments, includeName)
      .existing(includeComments, 'rosalution')
      .prompt();

  if (!attachment) {
    return;
  }

  try {
    // if attachment not existing in already attachment list
    await analysisStore.addDiscussionAttachment(attachment);
    console.log('The attachment was received');
    console.log(attachment);
  } catch (error) {
    await notificationDialog.title('Failure').confirmText('Ok').alert(error);
  }
}

/**
 * Toast to indicate text to the clipboard.
 *
 * @param {string} copiedText Text that was copied to the browser clipboard
 */
function copyToClipboard(copiedText) {
  toast.success(`Copied ${copiedText} to clipboard!`);
}

/**
 * When view is mounted, queries the analysis' state.
 */
onMounted(async () => {
  if ( analysisStore.analysis.name !== props.analysis_name) {
    analysisStore.clear();
  }
  await analysisStore.getAnalysis(props.analysis_name);
  toast = toastRef.value;
});
</script>

<style scoped>

app-content {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: var(--p-10)
}

app-header {
  position: sticky;
  top: 0px;
  z-index: 10;
  border-bottom: 4px solid var(--primary-background-color);
}

.save-modal {
  position: sticky;
  bottom: 0;
}
</style>
