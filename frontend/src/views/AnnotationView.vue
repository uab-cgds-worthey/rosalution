<template>
  <app-header>
    <AnnotationViewHeader
      :username="auth.getUsername()"
      :workflow_status="summary.latest_status"
      :analysisName="this.analysis_name"
      :genes="this.genomicUnits['genes']"
      :variants="this.genomicUnits['variants']"
      :activeGenomicUnits="this.active"
      :third_party_links="summary.third_party_links"
      @changed="this.onActiveGenomicUnitsChanged"
      @logout="this.onLogout"
    >
    </AnnotationViewHeader>
  </app-header>
  <app-content v-if="renderReady">
    <div class="sections">
      <AnnotationSection
        v-for="(section, index) in this.rendering" :key="`${section.type}-${section.anchor}-${index}`"
        :header="sectionHeader(section.header)" v-bind="section.props"
        :id="`${section.anchor}`" @attach-image="this.attachAnnotationImage"
        :writePermissions="auth.hasWritePermissions()"
      >
        <template #headerDatasets>
          <component
              v-for="(headerDatasetConfig, index) in section.header_datasets"
              :key="`${headerDatasetConfig.dataset}-${index}`"
              :is="headerDatasetConfig.type"
              :value="annotations[headerDatasetConfig.dataset]"
              v-bind="headerDatasetConfig.props"
              :data-test="headerDatasetConfig.dataset"
            />
        </template>
        <template #default>
          <div v-for="(row, index) in section.rows" :key="`row-${index}`" :class="row.class" class="grid-row-span">
            <component
                v-for="(datasetConfig, index) in row.datasets"
                :key="`${datasetConfig.dataset}-${index}`"
                :is="datasetConfig.type"
                :dataSet="datasetConfig.dataset"
                :genomicType="datasetConfig.genomicType"
                v-bind="buildProps(datasetConfig)"
                :value="annotations[datasetConfig.dataset]"
                :data-test="datasetConfig.dataset"
                :writePermissions="auth.hasWritePermissions()"
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
  </app-content>
  <AnnotationSidebar class="sidebar" :section-anchors="sectionAnchors"></AnnotationSidebar>
</template>

<script>
import Analyses from '@/models/analyses.js';
import Annotations from '@/models/annotations.js';

import AnnotationSection from '@/components/AnnotationView/AnnotationSection.vue';
import AnnotationSidebar from '@/components/AnnotationView/AnnotationSidebar.vue';
import AnnotationViewHeader from '@/components/AnnotationView/AnnotationViewHeader.vue';

import CardDataset from '@/components/AnnotationView/CardDataset.vue';
import ClinvarDataset from '@/components/AnnotationView/ClinvarDataset.vue';
import IconLinkoutDataset from '@/components/AnnotationView/IconLinkoutDataset.vue';
import ImagesDataset from '@/components/AnnotationView/ImagesDataset.vue';
import ScoreDataset from '@/components/AnnotationView/ScoreDataset.vue';
import SetDataset from '@/components/AnnotationView/SetDataset.vue';
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
    CardDataset,
    ClinvarDataset,
    IconLinkoutDataset,
    ImagesDataset,
    InputDialog,
    NotificationDialog,
    ScoreDataset,
    SetDataset,
    TextDataset,
    TranscriptDatasets,
    TagDataset,
  },
  props: {
    analysis_name: {
      type: String,
      required: true,
    },
  },
  data: function() {
    return {
      auth: authStore,
      rendering: [],
      annotations: {},
      active: {
        'gene': history.state.gene || '',
        'variant': history.state.variant || '',
      },
      genomicUnits: {
        'genes': {},
        'variants': [],
      },
      summary: {sections: []},
    };
  },
  computed: {
    renderReady() {
      return !( Object.keys(this.annotations).length === 0 || this.rendering.length === 0 );
    },
    sectionAnchors() {
      return this.rendering.map((section) => {
        return section.anchor;
      });
    },
    activeVariantWithRemovedProtein() {
      return this.active.variant.replace(/\(.*/, '');
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
      return header in this.active ? this.active[header] : header;
    },
    buildProps(datasetConfig) {
      return {
        ...datasetConfig.props,
        ...('linkout_dataset' in datasetConfig) && {linkout: this.annotations[datasetConfig['linkout_dataset']]},
      };
    },
    async onLogout() {
      this.$router.push({name: 'logout'});
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
        {
          ...await Annotations.getAnnotations(
              this.analysis_name, this.active.gene, this.activeVariantWithRemovedProtein,
          ),
        };
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

      const genomicUnit = genomicUnitType.includes('gene') ? this.active.gene : this.activeVariantWithRemovedProtein;

      const annotation = {
        genomic_unit_type: genomicUnitType,
        annotation_data: attachment.data,
      };

      try {
        const updatedAnnotation = await Annotations.attachAnnotationImage(genomicUnit, dataSet, annotation);

        if (!this.annotations[dataSet]) {
          this.annotations[dataSet] = [...updatedAnnotation];
        } else {
          this.annotations[dataSet].splice(0);
          this.annotations[dataSet].push(...updatedAnnotation);
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
        const updatedAnnotation = await Annotations.updateAnnotationImage(genomicUnit, dataSet, fileId, annotation);
        this.annotations[dataSet].splice(0);
        this.annotations[dataSet].push(...updatedAnnotation);
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

  grid-row: 2 / -2;
  grid-column: 1 / -2;
}

app-header {
  position: sticky;
  top:0px;
  z-index: 10;

  border: 4px solid var(--primary-background-color);
}

.sidebar {
  grid-row: 2 / -2;
  grid-column: -2 / -1;
  position: sticky;
  height: 90vh;
  top: 4rem;
  /* flex: 0 0 12.5rem; */
}

.sections {
  display: flex;
  flex-direction: column;
  flex: 1;
  gap: var(--p-10);
}

.fill-horizontal {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  flex-wrap: wrap;
}


</style>
