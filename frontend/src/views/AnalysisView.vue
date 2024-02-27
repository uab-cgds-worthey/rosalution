<template>
  <div>
    <app-header>
      <AnalysisViewHeader
        :actions="this.menuActions"
        :titleText="analysis.name"
        :sectionAnchors="this.sectionsHeaders"
        :username="auth.getUsername()"
        :workflow_status="analysis.latest_status"
        @logout="this.onLogout"
        :third_party_links="analysis.third_party_links"
        data-test="analysis-view-header"
      >
      </AnalysisViewHeader>
      <Toast data-test="toast" />
    </app-header>
    <app-content>
      <GeneBox
        v-for="genomicUnit in genomicUnitsList"
        :key="genomicUnit.id"
        :name="this.analysis_name"
        :gene="genomicUnit.gene"
        :transcripts="genomicUnit.transcripts"
        :variants="genomicUnit.variants"
        @clipboard-copy="this.copyToClipboard"
      />
      <SectionBox
        v-for="(section) in sectionsList"
        :id="section.header.replace(' ', '_')"
        :key="`${section.header}`"
        :analysis_name="this.analysis_name"
        :header="section.header"
        :content="section.content"
        :attachmentField="section.attachment_field"
        :writePermissions="auth.hasWritePermissions()"
        :edit="this.edit"
        @attach-image="this.attachSectionImage"
        @update-image="this.updateSectionImage"
        @update:content-row="this.onAnalysisContentUpdated"
        @download="this.downloadSupportingEvidence"
      />
      <DiscussionSection
        id="Discussion"
        :discussions="this.discussions"
        :userClientId="auth.getClientId()"
        :actions="this.discussionContextActions"
        @discussion:new-post="this.addDiscussionPost"
        @discussion:edit-post="this.editDiscussionPost"
        @discussion:delete-post="this.deleteDiscussionPost"
      />
      <SupplementalFormList
        id="Supporting_Evidence"
        :attachments="this.attachments"
        :writePermissions="auth.hasWritePermissions()"
        @open-modal="this.addSupportingEvidence"
        @delete="this.removeSupportingEvidence"
        @edit="this.editSupportingEvidence"
        @download="this.downloadSupportingEvidence"
      />
      <InputDialog />
      <NotificationDialog data-test="notification-dialog" />
      <SaveModal
        class="save-modal"
        v-if="this.edit"
        @canceledit="this.cancelAnalysisChanges"
        @save="this.saveAnalysisChanges"
      />
    </app-content>
  </div>
</template>

<script>
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
import {StatusType} from '@/config.js';

export default {
  name: 'analysis-view',
  components: {
    AnalysisViewHeader,
    SectionBox,
    GeneBox,
    InputDialog,
    NotificationDialog,
    Toast,
    SupplementalFormList,
    SaveModal,
    DiscussionSection,
  },
  props: ['analysis_name'],
  data: function() {
    return {
      auth: authStore,
      analysis: {
        name: '',
        sections: [],
      },
      updatedContent: {},
      edit: false,
    };
  },
  computed: {
    sectionsHeaders() {
      const sections = this.analysis.sections.map((section) => {
        return section.header;
      });
      sections.push('Discussion');
      sections.push('Supporting Evidence');
      return sections;
    },
    menuActions() {
      const actionChoices = [];

      actionChoices.push({
        icon: 'paperclip',
        text: 'Attach',
        operation: this.addSupportingEvidence,
      });

      if ( !this.auth.hasWritePermissions() ) {
        return actionChoices;
      }

      const prependingActions = [];

      prependingActions.push({
        icon: 'pencil',
        text: 'Edit',
        operation: () => {
          if (!this.edit) {
            toast.success('Edit mode has been enabled.');
          } else {
            toast.info('Edit mode has been disabled and changes have not been saved.');
          }
          this.edit = !this.edit;
        },
      });

      if (this.analysis.latest_status === 'Preparation') {
        prependingActions.push({
          icon: StatusType['Ready'].icon,
          text: 'Mark Ready',
          operation: () => {
            this.pushAnalysisEvent(Analyses.EventType.READY);
          },
        });
      } else if (this.analysis.latest_status === 'Ready') {
        prependingActions.push({
          icon: StatusType['Active'].icon,
          text: 'Mark Active',
          operation: () => {
            this.pushAnalysisEvent(Analyses.EventType.OPEN);
          },
        });
      } else {
        prependingActions.push({
          icon: StatusType['Approved'].icon,
          text: 'Approve',
          operation: () => {
            this.pushAnalysisEvent(Analyses.EventType.APPROVE);
          },
        }, {
          icon: StatusType['On-Hold'].icon,
          text: 'Hold',
          operation: () => {
            this.pushAnalysisEvent(Analyses.EventType.HOLD);
          },
        }, {
          icon: StatusType['Declined'].icon,
          text: 'Decline',
          operation: () => {
            this.pushAnalysisEvent(Analyses.EventType.DECLINE);
          },
        });
      }
      prependingActions.push({divider: true});
      actionChoices.unshift(...prependingActions);

      actionChoices.push({
        text: 'Attach Monday.com',
        operation: this.addMondayLink,
      });

      actionChoices.push({
        text: 'Connect PhenoTips',
        operation: this.addPhenotipsLink,
      });

      return actionChoices;
    },
    discussionContextActions() {
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
    },
    sectionsList() {
      return this.analysis.sections;
    },
    attachments() {
      return this.analysis.supporting_evidence_files;
    },
    discussions() {
      return this.analysis.discussions;
    },
    genomicUnitsList() {
      return this.analysis.genomic_units;
    },
  },
  created() {
    this.getAnalysis();
  },
  methods: {
    async getAnalysis() {
      this.analysis = await Analyses.getAnalysis(this.analysis_name);
    },
    onAnalysisContentUpdated(contentRow) {
      if (typeof(contentRow.type) !== 'undefined' && 'supporting-evidence' === contentRow.type ) {
        this.fieldSectionAttachmentChanged(contentRow);
        return;
      }

      if (!(contentRow.header in this.updatedContent)) {
        this.updatedContent[contentRow.header] = {};
      }

      this.updatedContent[contentRow.header][contentRow.field] = contentRow.value;
    },
    async saveAnalysisChanges() {
      const updatedSections = await Analyses.updateAnalysisSections(
          this.analysis_name,
          this.updatedContent,
      );
      this.analysis.sections.splice(0);
      this.analysis.sections.push(...updatedSections);
      location.reload();
      this.updatedContent = {};
      this.edit = false;
      toast.success('Analysis updated successfully.');
    },
    cancelAnalysisChanges() {
      this.edit = false;
      this.updatedContent = {};
      toast.info('Edit mode has been disabled and changes have not been saved.');
    },
    async attachSectionImage(sectionName, field) {
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
        const updatedSectionField = await Analyses.attachSectionImage(
            this.analysis_name,
            sectionName,
            field,
            attachment.data,
        );

        const sectionWithReplacedField = this.replaceFieldInSection(sectionName, updatedSectionField);
        this.replaceAnalysisSection(sectionWithReplacedField);
      } catch (error) {
        await notificationDialog.title('Failure').confirmText('Ok').alert(error);
      }
    },
    async updateSectionImage(fileId, sectionName, field) {
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
        await this.removeSectionImage(fileId, sectionName, field);
        return;
      }

      try {
        const updatedSectionField = await Analyses.updateSectionImage(
            this.analysis_name,
            sectionName,
            field,
            fileId,
            attachment.data,
        );

        const sectionWithReplacedField = this.replaceFieldInSection(sectionName, updatedSectionField);
        this.replaceAnalysisSection(sectionWithReplacedField);
      } catch (error) {
        await notificationDialog.title('Failure').confirmText('Ok').alert(error);
      }
    },
    async removeSectionImage(fileId, sectionName, field) {
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
        const updatedSectionField =
          await Analyses.removeSectionAttachment(this.analysis_name, sectionName, field, fileId);

        const sectionWithReplacedField = this.replaceFieldInSection(sectionName, updatedSectionField);
        this.replaceAnalysisSection(sectionWithReplacedField);
      } catch (error) {
        await notificationDialog.title('Failure').confirmText('Ok').alert(error);
      }
    },
    async fieldSectionAttachmentChanged(contentRow) {
      const operations = {
        'attach': this.addSectionAttachment,
        'delete': this.removeSectionAttachment,
      };

      if (!Object.hasOwn(operations, contentRow.operation)) {
        // Warning here that the operation is invalid and move on
        return;
      }

      operations[contentRow.operation](contentRow.header, contentRow.field, contentRow.value);
    },
    async addSectionAttachment(section, field, evidence) {
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
            this.analysis_name,
            section,
            field,
            attachment,
        );
        const sectionWithReplacedField = this.replaceFieldInSection(section, updatedSectionField);
        this.replaceAnalysisSection(sectionWithReplacedField);
      } catch (error) {
        console.error('Updating the analysis did not work');
      }
    },
    async removeSectionAttachment(section, field, attachment) {
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
          await Analyses.removeSectionAttachment(this.analysis_name, section, field, attachment.attachment_id);
        const sectionWithReplacedField = this.replaceFieldInSection(section, updatedSectionField);

        this.replaceAnalysisSection(sectionWithReplacedField);
      } catch (error) {
        await notificationDialog.title('Failure').confirmText('Ok').alert(error);
      }
    },
    async addSupportingEvidence() {
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
        const updatedAnalysisAttachments = await Analyses.attachSupportingEvidence(
            this.analysis_name,
            attachment,
        );
        this.analysis.supporting_evidence_files.splice(0);
        this.analysis.supporting_evidence_files.push(
            ...updatedAnalysisAttachments,
        );
      } catch (error) {
        await notificationDialog.title('Failure').confirmText('Ok').alert(error);
      }
    },
    async editSupportingEvidence(attachment) {
      const updatedAttachment = await inputDialog
          .confirmText('Update')
          .cancelText('Cancel')
          .edit(attachment)
          .prompt();

      if (!updatedAttachment) {
        return;
      }

      try {
        const updatedAnalysisAttachments = await Analyses.updateSupportingEvidence(
            this.analysis_name,
            updatedAttachment,
        );
        this.analysis.supporting_evidence_files.splice(0);
        this.analysis.supporting_evidence_files.push(
            ...updatedAnalysisAttachments,
        );
      } catch (error) {
        await notificationDialog.title('Failure').confirmText('Ok').alert(error);
      }
    },
    async removeSupportingEvidence(attachmentToDelete) {
      const confirmedDelete = await notificationDialog
          .title('Delete Supporting Information?')
          .confirmText('Delete')
          .cancelText('Cancel')
          .confirm('Deleting this item will remove it from the supporting evidence list.');

      if (!confirmedDelete) {
        return;
      }

      try {
        await Analyses.removeSupportingEvidence(
            this.analysis_name,
            attachmentToDelete.attachment_id,
        );
        const attachmentIndex = this.attachments.findIndex((attachment) => {
          return attachment.name == attachmentToDelete.name;
        });
        this.analysis.supporting_evidence_files.splice(attachmentIndex, 1);
      } catch (error) {
        await notificationDialog.title('Failure').confirmText('Ok').alert(error);
      }
    },
    downloadSupportingEvidence(attachmentToDownload) {
      Analyses.downloadSupportingEvidence(
          attachmentToDownload.attachment_id,
          attachmentToDownload.name,
      );
    },
    async onLogout() {
      this.$router.push({name: 'logout'});
    },
    async addMondayLink() {
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
            this.analysis_name,
            'monday_com',
            mondayLink.data,
        );

        this.analysis = {...this.analysis, ...updatedAnalysis};
      } catch (error) {
        console.error('Updating the analysis did not work', error);
      }
    },
    async addPhenotipsLink() {
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
            this.analysis_name,
            'phenotips_com',
            phenotipsLink.data,
        );

        this.analysis = {...this.analysis, ...updatedAnalysis};
      } catch (error) {
        console.error('Updating the analysis did not work', error);
      }
    },
    async pushAnalysisEvent(eventType) {
      try {
        const updatedAnalysis = await Analyses.pushAnalysisEvent(this.analysis_name, eventType);
        this.analysis = {...this.analysis, ...updatedAnalysis};
        toast.success(`Analysis event '${eventType}' successful.`);
      } catch (error) {
        toast.error(`Error updating the event '${eventType}'.`);
      }
    },
    async addDiscussionPost(newPostContent) {
      const discussions = await Analyses.postNewDiscussionThread(this.analysis['name'], newPostContent);
      this.analysis.discussions = discussions;
    },
    async editDiscussionPost(postId, postContent) {
      const analysisName = this.analysis_name;
      const discussions = await Analyses.editDiscussionThreadById(analysisName, postId, postContent);
      this.analysis.discussions = discussions;
    },
    async deleteDiscussionPost(postId) {
      const analysisName = this.analysis_name;
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
        this.analysis.discussions = discussions;
      } catch (error) {
        await notificationDialog.title('Failure').confirmText('Ok').alert(error);
      }
    },
    replaceFieldInSection(sectionName, updatedField) {
      const sectionToUpdate = this.sectionsList.find((section) => {
        return section.header == sectionName;
      });

      const fieldToUpdate = sectionToUpdate.content.find((row) => {
        return row.field == updatedField['field'];
      });

      fieldToUpdate.value = updatedField.value;

      return sectionToUpdate;
    },
    replaceAnalysisSection(sectionToReplace) {
      const originalSectionIndex = this.analysis.sections.findIndex(
          (section) => section.header == sectionToReplace.header,
      );
      this.analysis.sections.splice(originalSectionIndex, 1, sectionToReplace);
    },
    copyToClipboard(copiedText) {
      toast.success(`Copied ${copiedText} to clipboard!`);
    },
  },
};
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
