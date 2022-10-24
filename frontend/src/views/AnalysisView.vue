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
          @update:content-row="this.onAnalysisContentUpdated"
        />
        <SupplementalFormList
          id="Supporting_Evidence"
          :attachments="this.attachments"
          @open-modal="this.addSupportingEvidence"
          @delete="this.onDeleteAttachmentEvent"
          @edit="this.onEditAttachment"
        />
        <InputDialog />
        <NotificationDialog
          data-test="notification-dialog"
        />
        <SaveModal
        class="save-modal"
        v-if="this.edit"
        @canceledit="this.onAnalysisSaveCancel"
        @save="this.onAnalysisSave"
        />
      </app-content>
  </div>
</template>

<script>
import Analyses from '@/models/analyses.js';
import AnalysisViewHeader from '../components/AnalysisView/AnalysisViewHeader.vue';
import SectionBox from '../components/AnalysisView/SectionBox.vue';
import GeneBox from '../components/AnalysisView/GeneBox.vue';
import InputDialog from '../components/Dialogs/InputDialog.vue';
import NotificationDialog from '@/components/Dialogs/NotificationDialog.vue';
import SupplementalFormList from '@/components/AnalysisView/SupplementalFormList.vue';
import SaveModal from '../components/AnalysisView/SaveModal.vue';

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
    async attachSectionImage(updatedSectionName) {
      const includeComments = false;
      const attachment = await inputDialog
          .confirmText('Attach')
          .cancelText('Cancel')
          .file(includeComments, 'file', '.png, .jpg, .jpeg, .bmp')
          .prompt();

      if (!attachment) {
        return;
      }

      const updatedAnalysis = await Analyses.attachSectionBoxImage(this.analysis_name, attachment.data);
      const updatedSection = updatedAnalysis['sections'].find((section) => section.header == updatedSectionName);
      const editedSectionIndex = this.sectionsList.findIndex((section) => section.header == updatedSectionName);
      this.analysis.sections.splice(editedSectionIndex, 1, updatedSection);
      // Needed to create this uptick because the replaced element wasn't getting detected to
      // cause it to update this still make cause issue with the edit mode and will need to re-evaluate
      this.uptickForceRenderKey();
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
    async onDeleteAttachmentEvent(attachmentToDelete) {
      const confirmedDelete = await notificationDialog
          .title('Delete Supporting Information?')
          .confirmText('Delete')
          .cancelText('Cancel')
          .confirm('Deleting this item will remove it from the supporting evidence list.');

      if (!confirmedDelete) {
        return;
      }

      const attachmentIndex = this.attachments.findIndex((attachment) => {
        return attachment.name == attachmentToDelete.name;
      });
      this.analysis.supporting_evidence_files.splice(attachmentIndex, 1);
    },
    async onEditAttachment(attachment) {
      const updatedAttachment = await inputDialog
          .confirmText('Update')
          .cancelText('Cancel')
          .edit(attachment)
          .prompt('Temp for file upload');

      if (!updatedAttachment) {
        return;
      }
    },
    async onLogout() {
      await this.store.logout();
      this.$router.push({path: '/rosalution/login'});
    },
    uptickForceRenderKey() {
      this.forceRenderComponentKey += 1;
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
