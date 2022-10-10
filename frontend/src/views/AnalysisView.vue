<template>
  <div>
      <app-header>
        <AnalysisViewHeader
          :actions="this.menuActions"
          :titleText="this.analysis_name"
          :sectionAnchors="this.sectionsHeaders"
          :username="this.username"
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
          v-for="section in sectionsList"
          :id="section.header.replace(' ', '_')"
          :key="section.id"
          :analysis_name="this.analysis_name"
          :header="section.header"
          :content="section.content"
          :edit = "this.edit"
        />
        <SupplementalFormList
          id="Supplemental_Attachments"
          :attachments="this.attachments"
          @open-modal="this.toggleAttachmentModal"
          @delete="this.onDeleteAttachmentEvent"
          @edit="this.onEditAttachment"
        />
        <ModalDialog
          v-if="showAttachmentModal"
          @save="this.onAddAttachment"
          @close="this.toggleAttachmentModal()"
          data-test="modal-dialog"
        />
        <Dialog
          data-test="confirmation-dialog"
        />
        <SaveModal
        class="save-modal"
        v-if="this.edit"
        @canceledit="this.edit=false"
        />
      </app-content>
  </div>
</template>

<script>
import Analyses from '@/models/analyses.js';
import AnalysisViewHeader from '../components/AnalysisView/AnalysisViewHeader.vue';
import SectionBox from '../components/AnalysisView/SectionBox.vue';
import GeneBox from '../components/AnalysisView/GeneBox.vue';
import ModalDialog from '@/components/AnalysisView/ModalDialog.vue';
import Dialog from '../components/Dialog.vue';
import SupplementalFormList from '../components/AnalysisView/SupplementalFormList.vue';
import Auth from '../models/authentication.js';
import SaveModal from '../components/AnalysisView/SaveModal.vue';

import dialog from '@/dialog.js';

export default {
  name: 'analysis-view',
  components: {
    AnalysisViewHeader,
    SectionBox,
    GeneBox,
    Dialog,
    ModalDialog,
    SupplementalFormList,
    SaveModal,
  },
  props: ['analysis_name'],
  data: function() {
    return {
      username: '',
      analysis: {},
      sectionsList: [],
      genomicUnitsList: [],
      attachments: [],
      menuActions: [
        {icon: 'pencil', text: 'Edit', operation: () => {
          this.edit = !this.edit;
        }, divider: true},
        {icon: 'paperclip', text: 'Attach', operation: this.toggleAttachmentModal},
      ],
      showAttachmentModal: false,
      edit: false,
    };
  },
  computed: {
    sectionsHeaders() {
      const sections = this.sectionsList.map((section) => {
        return section.header;
      });
      sections.push('Supplemental Attachments');
      return sections;
    },
  },
  created() {
    this.getUsername();
    this.getAnalysis();
  },
  methods: {
    async getUsername() {
      const fetchUser = await Auth.getUser();
      this.username = fetchUser['username'];
    },
    async getAnalysis() {
      this.analysis = {...await Analyses.getAnalysis(this.analysis_name)};
      this.getSections();
      this.getGenomicUnits();
      this.getAttachments();
    },
    getSections() {
      this.sectionsList=this.analysis.sections;
    },
    getGenomicUnits() {
      this.genomicUnitsList=this.analysis.genomic_units;
    },
    getAttachments() {
      this.attachments = this.analysis.supporting_evidence_files;
    },
    toggleAttachmentModal() {
      this.showAttachmentModal = !this.showAttachmentModal;
    },
    async onAddAttachment(attachment) {
      try {
        const updatedAnalysis = await Analyses.attachSupportingEvidence(this.analysis_name, attachment);
        this.attachments.splice(0);
        this.attachments.push(...updatedAnalysis.supporting_evidence_files);
      } catch (error) {
        console.error('Updating the anlayis did not work');
      }

      this.toggleAttachmentModal();
    },
    async onDeleteAttachmentEvent(attachmentToDelete) {
      const confirmedDelete = await dialog
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
      this.attachments.splice(attachmentIndex, 1);
    },
    onEditAttachment(attachment) {
      /* will update the props going into the modal component to edit this attachment */
    },
    async onLogout() {
      await Auth.logout();
      this.$router.push({path: '/rosalution/login'});
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
