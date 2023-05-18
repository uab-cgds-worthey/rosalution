<template>
  <app-header>
    <AnnotationViewHeader
      :username="username"
      :workflow_status="summary.latest_status"
      :analysisName="this.analysis_name"
      :genes="this.genomicUnits['genes']"
      :variants="this.genomicUnits['variants']"
      :activeGenomicUnits="this.active"
      :third_party_links="summary.third_party_links"
      @changed="this.onActiveGenomicUnitsChanged"
    >
    </AnnotationViewHeader>
  </app-header>
  <app-content>
    <div class="sections">
      <AnnotationSection
        v-for="(section, index) in this.rendering" :key="`${section.type}-${section.anchor}-${index}`"
        :header="sectionHeader(section.header)" v-bind="section.props"
        :id="`${section.anchor}`" @attach-image="this.attachAnnotationImage"
      >
        <template #headerDatasets>
          <component
              v-for="(headerDatasetConfig, index) in section.header_datasets"
              :key="`${headerDatasetConfig.dataset}-${index}`"
              :is="headerDatasetConfig.type"
              v-bind="headerDatasetConfig.props"
              :value="annotations[headerDatasetConfig.dataset]"
              :data-test="headerDatasetConfig.dataset"
            />
        </template>
        <template #default>
          <div v-for="(row, index) in section.rows" :key="`row-${index}`">
            <component
                v-for="(datasetConfig, index) in row.datasets"
                :key="`${datasetConfig.dataset}-${index}`"
                :is="datasetConfig.type"
                :dataSet="datasetConfig.dataset"
                :genomicType="datasetConfig.genomicType"
                v-bind="buildProps(datasetConfig)"
                :value="annotations[datasetConfig.dataset]"
                :data-test="datasetConfig.dataset"
                @update-annotation-image="this.updateAnnotationImage"
              />
          </div>
        </template>
      </AnnotationSection>
      <InputDialog />
      <NotificationDialog
          data-test="notification-dialog"
        />
    </div>
    <AnnotationSidebar class="sidebar" :section-anchors="sectionAnchors"></AnnotationSidebar>
  </app-content>
</template>

<script>
import Analyses from '@/models/analyses.js';
import Annotations from '@/models/annotations.js';

import AnnotationSection from '@/components/AnnotationView/AnnotationSection.vue';
import AnnotationSidebar from '@/components/AnnotationView/AnnotationSidebar.vue';
import AnnotationViewHeader from '@/components/AnnotationView/AnnotationViewHeader.vue';

import ClinvarDataset from '@/components/AnnotationView/ClinvarDataset.vue';
import IconLinkoutDataset from '@/components/AnnotationView/IconLinkoutDataset.vue';
import ImagesDataset from '@/components/AnnotationView/ImagesDataset.vue';
import ScoreDataset from '@/components/AnnotationView/ScoreDataset.vue';
import TextDataset from '@/components/AnnotationView/TextDataset.vue';
import TranscriptDatasets from '@/components/AnnotationView/TranscriptDatasets.vue';
import InputDialog from '@/components/Dialogs/InputDialog.vue';
import NotificationDialog from '@/components/Dialogs/NotificationDialog.vue';
import TagDataset from '@/components/AnnotationView/TagDataset.vue';

import inputDialog from '@/inputDialog.js';
import notificationDialog from '@/notificationDialog.js';

import {authStore} from '@/stores/authStore.js';

export default {
  name: 'annotation-view',
  components: {
    AnnotationSection,
    AnnotationSidebar,
    AnnotationViewHeader,
    ClinvarDataset,
    IconLinkoutDataset,
    ImagesDataset,
    InputDialog,
    NotificationDialog,
    ScoreDataset,
    TextDataset,
    TranscriptDatasets,
    TagDataset,
  },
  props: {
    analysis_name: {
      type: String,
      required: true,
    },
    gene: {
      type: String,
      required: false,
      default: '',
    },
    variant: {
      type: String,
      required: false,
      default: '',
    },
  },
  data: function() {
    return {
      store: authStore,
      rendering: [],
      annotations: {},
      active: {
        'gene': this.gene,
        'variant': this.variant,
      },
      genomicUnits: {
        'genes': {},
        'variants': [],
      },
      summary: {sections: []},
    };
  },
  computed: {
    username() {
      return this.store.state.username;
    },
    sectionAnchors() {
      return this.rendering.map((section) => {
        return section.anchor;
      });
    },
  },
  async created() {
    await this.getGenomicUnits();
    await this.getRenderingConfiguration();
    await this.getAnnotations();
    await this.getSummaryByName();
  },
  methods: {
    async getSummaryByName() {
      this.summary = await Analyses.getSummaryByName(this.analysis_name);
    },
    sectionHeader(header) {
      return header in this ? this.active[header] : header;
    },
    buildProps(datasetConfig) {
      return {
        ...datasetConfig.props,
        ...('linkout_dataset' in datasetConfig) && {linkout: this.annotations[datasetConfig['linkout_dataset']]},
      };
    },
    async getGenomicUnits() {
      this.genomicUnits = {...await Analyses.getGenomicUnits(this.analysis_name)};
      if (this.active.gene === '') {
        const genes = Object.keys(this.genomicUnits['genes']);
        this.active.gene = genes[0];
        if (this.genomicUnits['genes'][this.active.gene].length !== 0) {
          this.active.variant = this.genomicUnits['genes'][this.active.gene][0];
        }
      }
    },
    async getRenderingConfiguration() {
      this.rendering.push(...await Analyses.getAnnotationConfiguration(this.analysis_name));
    },
    async getAnnotations() {
      this.annotations =
        {...await Annotations.getAnnotations(this.analysis_name, this.active.gene, this.active.variant)};
    },
    async onActiveGenomicUnitsChanged(genomicUnitsChanged) {
      this.active.gene = genomicUnitsChanged.gene;
      this.active.variant = genomicUnitsChanged.variant;
      this.annotations = {};
      await(this.getAnnotations());
    },
    async attachAnnotationImage(dataSet, genomicUnitType) {
      const includeComments = false;
      const attachment = await inputDialog
          .confirmText('Attach')
          .cancelText('Cancel')
          .file(includeComments, 'file', '.png, .jpg, .jpeg, .bmp')
          .prompt();

      if (!attachment) {
        return;
      }

      const genomicUnit = genomicUnitType.includes('gene') ? this.active.gene : this.active.variant.replace(/\(.*/, '');

      const annotation = {
        genomic_unit_type: genomicUnitType,
        annotation_data: attachment.data,
      };

      try {
        const updatedAnnotation = await Annotations.attachAnnotationImage(genomicUnit, dataSet, annotation);

        if (!this.annotations[dataSet]) {
          this.annotations[dataSet] = [{file_id: updatedAnnotation['image_id'], created_date: ''}];
        } else {
          this.annotations[dataSet].push({file_id: updatedAnnotation['image_id'], created_date: ''});
        }
      } catch (error) {
        await notificationDialog
            .title('Failure')
            .confirmText('Ok')
            .alert(error);
      }
    },
    async updateAnnotationImage(fileId, dataSet, genomicUnitType) {
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

      const genomicUnit = genomicUnitType.includes('gene') ? this.active.gene : this.active.variant.replace(/\(.*/, '');

      const annotation = {
        genomic_unit_type: genomicUnitType,
        annotation_data: attachment.data,
      };

      if ('DELETE' == attachment) {
        await this.removeAnnotationImage(genomicUnit, dataSet, fileId, annotation);
        return;
      }

      try {
        const that = this;
        await Annotations.updateAnnotationImage(genomicUnit, dataSet, fileId, annotation).then(function(response) {
          that.annotations[dataSet].forEach((elem) => {
            if (elem['file_id'] == fileId) {
              elem['file_id'] = response['image_id'];
            }
          });
        });
      } catch (error) {
        await notificationDialog
            .title('Failure')
            .confirmText('Ok')
            .alert(error);
      }
    },
    async removeAnnotationImage(genomicUnit, dataSet, fileId, annotation) {
      const confirmedDelete = await notificationDialog
          .title(`Remove Annotation attachment`)
          .confirmText('Remove')
          .cancelText('Cancel')
          .confirm('This operation will permanently remove the image. Are you sure you want to remove?');

      if (!confirmedDelete) {
        return;
      }

      try {
        await Annotations.removeAnnotationImage(genomicUnit, dataSet, fileId, annotation);
      } catch (error) {
        await notificationDialog
            .title('Failure')
            .confirmText('Ok')
            .alert(error);
      }

      this.annotations[dataSet] = this.annotations[dataSet].filter( (obj) => {
        return obj.file_id !== fileId;
      });
    },
  },
};
</script>

<style scoped>

app-content {
  display: flex;
  flex-direction: row;
  gap: var(--p-10);
}

app-header {
  position: sticky;
  top:0px;
  z-index: 10;
}

.sections {
  flex: 7 1 auto;
}

.sidebar {
  position: sticky;
  height: 90vh;
  top: 4rem;
  flex: 1 1 auto;
}

</style>
