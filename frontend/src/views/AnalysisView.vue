<template>
  <div>
      <app-header>
        <AnalysisViewHeader
          :actions="this.menuActions"
          :titleText="this.analysis_name"
          :sectionAnchors="this.sectionsHeaders"
          :username="username"
          @logout="this.onLogout"
          data-test="analysis-view-header">
        </AnalysisViewHeader>
      </app-header>
      <app-content>
        <GeneBox
          v-for="genomicUnit in genomicUnitsList"
          :key="genomicUnit.id"
          :name="this.analysis_name"
          :gene="genomicUnit.gene"
          :transcripts="genomicUnit.transcripts"
          :variants="genomicUnit.variants"
        />
        <SectionBox
          v-for="(section, index) in sectionsList"
          :id="section.header.replace(' ', '_')"
          :key="`${section.header}-${index}-${forceRenderComponentKey}`"
          :analysis_name="this.analysis_name"
          :header="section.header"
          :content="section.content"
          :edit = "this.edit"
          @attach-image="this.attachSectionImage"
          @update-image="this.updateSectionImage"
          @update:content-row="this.onAnalysisContentUpdated"
        />
        <SupplementalFormList
          id="Supporting_Evidence"
          :attachments="this.attachments"
          @open-modal="this.addSupportingEvidence"
          @delete="this.removeSupportingEvidence"
          @edit="this.editSupportingEvidence"
          @download="this.downloadSupportingEvidence"
        />
        <InputDialog />
        <NotificationDialog
          data-test="notification-dialog"
        />
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
import SupplementalFormList from '@/components/AnalysisView/SupplementalFormList.vue';
import SaveModal from '@/components/AnalysisView/SaveModal.vue';

import inputDialog from '@/inputDialog.js';
import notificationDialog from '@/notificationDialog.js';

import {authStore} from '@/stores/authStore.js';

export default {
  name: 'analysis-view',
  components: {
    AnalysisViewHeader,
    SectionBox,
    GeneBox,
    InputDialog,
    NotificationDialog,
    SupplementalFormList,
    SaveModal,
  },
  props: ['analysis_name'],
  data: function() {
    return {
      store: authStore,
      analysis: {sections: []},
      updatedContent: {},
      menuActions: [
        {icon: 'pencil', text: 'Edit', operation: () => {
          this.edit = !this.edit;
        }, divider: true},
        {icon: 'paperclip', text: 'Attach', operation: this.addSupportingEvidence},
        {text: 'Attach Monday.com', operation: this.addMondayLink},
        {text: 'Connect PhenoTips'},
      ],
      edit: false,
      forceRenderComponentKey: 0,
    };
  },
  computed: {
    username() {
      return this.store.state.username;
    },
    sectionsHeaders() {
      const sections = this.analysis.sections.map((section) => {
        return section.header;
      });
      sections.push('Supporting Evidence');
      return sections;
    },
    sectionsList() {
      return this.analysis.sections;
    },
    attachments() {
      return this.analysis.supporting_evidence_files;
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
      this.analysis = {...await Analyses.getAnalysis(this.analysis_name)};
    },
    async attachSectionImage(sectionName) {
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
        const updatedSection = await Analyses.attachSectionImage(this.analysis_name, sectionName, attachment.data);
        this.replaceAnalysisSection(updatedSection);
        // Needed to create this uptick because the replaced element wasn't getting detected to
        // cause it to update this still make cause issue with the edit mode and will need to re-evaluate
        this.uptickSectionKeyToForceReRender();
      } catch (error) {
        await notificationDialog
            .title('Failure')
            .confirmText('Ok')
            .alert(error);
      }
    },
    async updateSectionImage(sectionName) {
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

      if ('DELETE' == attachment ) {
        await this.removeSectionImage(sectionName);
        this.uptickSectionKeyToForceReRender();
        return;
      }

      try {
        const updatedSection = await Analyses.updateSectionImage(this.analysis_name, sectionName, attachment.data);
        this.replaceAnalysisSection(updatedSection);

        // Needed to create this uptick because the replaced element wasn't getting detected to
        // cause it to update this still make cause issue with the edit mode and will need to re-evaluate
        this.uptickSectionKeyToForceReRender();
      } catch (error) {
        await notificationDialog
            .title('Failure')
            .confirmText('Ok')
            .alert(error);
      }
    },
    async removeSectionImage(sectionName) {
      const confirmedDelete = await notificationDialog
          .title(`Remove ${sectionName} attachment`)
          .confirmText('Remove')
          .cancelText('Cancel')
          .confirm('This operation will permanently remove the image. Are you sure you want to remove?');

      if (!confirmedDelete) {
        return;
      }

      try {
        await Analyses.removeSectionImage(this.analysis_name, sectionName);
        this.replaceAnalysisSection({'header': sectionName, 'content': []});
      } catch (error) {
        await notificationDialog
            .title('Failure')
            .confirmText('Ok')
            .alert(error);
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
        const updatedAnalysis = await Analyses.attachSupportingEvidence(this.analysis_name, attachment);
        this.analysis.supporting_evidence_files.splice(0);
        this.analysis.supporting_evidence_files.push(...updatedAnalysis.supporting_evidence_files);
      } catch (error) {
        console.error('Updating the analysis did not work');
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
        const updatedAnalysis = await Analyses.updateSupportingEvidence(this.analysis_name, updatedAttachment);
        this.analysis.supporting_evidence_files.splice(0);
        this.analysis.supporting_evidence_files.push(...updatedAnalysis.supporting_evidence_files);
      } catch (error) {
        console.error('Updating the analysis did not work');
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
        await Analyses.removeSupportingEvidence(this.analysis_name, attachmentToDelete.attachment_id);
        const attachmentIndex = this.attachments.findIndex((attachment) => {
          return attachment.name == attachmentToDelete.name;
        });
        this.analysis.supporting_evidence_files.splice(attachmentIndex, 1);
      } catch (error) {
        await notificationDialog
            .title('Failure')
            .confirmText('Ok')
            .alert(error);
      }
    },
    downloadSupportingEvidence(attachmentToDownload) {
      Analyses.downloadSupportingEvidence(attachmentToDownload.attachment_id, attachmentToDownload.name);
    },
    async saveAnalysisChanges() {
      const updatedAnalysis = await Analyses.updateAnalysisSections(this.analysis_name, this.updatedContent);
      this.analysis.sections.splice(0);
      this.analysis.sections.push(...updatedAnalysis.sections);
      this.updatedContent = {};
      this.edit=false;
      this.uptickSectionKeyToForceReRender();
    },
    cancelAnalysisChanges() {
      this.edit=false;
      this.updatedContent = {};
    },
    async onLogout() {
      this.$router.push({path: '/rosalution/logout'});
    },
    uptickSectionKeyToForceReRender() {
      this.forceRenderComponentKey += 1;
    },
    onAnalysisContentUpdated(contentRow) {
      if ( !(contentRow.header in this.updatedContent) ) {
        this.updatedContent[contentRow.header] = {};
      }

      this.updatedContent[contentRow.header][contentRow.field] = contentRow.value;
    },
    replaceAnalysisSection(sectionToReplace) {
      const originalSectionIndex = this.sectionsList.findIndex((section) => section.header == sectionToReplace.header);
      this.analysis.sections.splice(originalSectionIndex, 1, sectionToReplace);
    },
    async addMondayLink() {
      console.log('add monday link');
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
        console.log('mondayLink', mondayLink.data);
        await Analyses.attachThirdPartyLink(this.analysis_name, 'MONDAY_COM', mondayLink.data);
      } catch (error) {
        console.error('Updating the analysis did not work', error);
      }
    },
  },
};
</script>

<style scoped>

div {
  font-family: "Proxima Nova", sans-serif;
}

app-content {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  height: 100%;
}

app-header {
  position: sticky;
  top:0px;
  z-index: 10;
}

.save-modal {
  position:sticky;
  bottom: 0;
}

</style>
