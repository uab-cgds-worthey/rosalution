<template>
  <app-header>
    <AnnotationViewHeader
      :username="username"
      :analysisName="this.analysis_name"
      :genes="this.genomicUnits['genes']"
      :variants="this.genomicUnits['variants']"
      :activeGenomicUnits="this.active"
      @changed="this.onActiveGenomicUnitsChanged"
    >
    </AnnotationViewHeader>
  </app-header>
  <app-content>
    <div class="sections">
      <AnnotationSection
        v-for="(section, index) in this.rendering" :key="`${section.type}-${section.anchor}-${index}`"
        :header="sectionHeader(section.header)" v-bind="section.props"
        :id="`${section.anchor}`" @attach-image="this.attachSectionImage"
        :allowAttach="section.allowHeaderAttachImageDataset"
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
                v-bind="buildProps(datasetConfig)"
                :value="annotations[datasetConfig.dataset]"
                :data-test="datasetConfig.dataset"
              />
          </div>
        </template>
      </AnnotationSection>
      <InputDialog />
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
import ImageDataset from '@/components/AnnotationView/ImageDataset.vue';
import ScoreDataset from '@/components/AnnotationView/ScoreDataset.vue';
import TextDataset from '@/components/AnnotationView/TextDataset.vue';
import TranscriptDatasets from '@/components/AnnotationView/TranscriptDatasets.vue';
import InputDialog from '@/components/Dialogs/InputDialog.vue';

import inputDialog from '@/inputDialog.js';

import {authStore} from '@/stores/authStore.js';

export default {
  name: 'annotation-view',
  components: {
    AnnotationSection,
    AnnotationSidebar,
    AnnotationViewHeader,
    ClinvarDataset,
    IconLinkoutDataset,
    ImageDataset,
    ScoreDataset,
    TextDataset,
    TranscriptDatasets,
    InputDialog,
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
    this.getRenderingConfiguration();
    this.getAnnotations();
  },
  methods: {
    sectionHeader(header) {
      return header in this ? this.active[header] : header;
    },
    imageId(header) {
      if (this.annotations[header] != undefined) {
        return this.annotations[header];
      }

      return '';
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
    async attachSectionImage(updatedSectionName) {
      console.log(this.annotations)
      if(!this.annotations[updatedSectionName])
        console.log("Inuyasha")
      const includeComments = false;
      const attachment = await inputDialog
          .confirmText('Attach')
          .cancelText('Cancel')
          .file(includeComments, 'file', '.png, .jpg, .jpeg, .bmp')
          .prompt();

      if (!attachment) {
        return;
      }

      const isGeneAnnotation = !updatedSectionName.includes('Multi-Sequence');
      const annotation = {
        genomic_unit: isGeneAnnotation ? this.active.gene : this.active.variant.replace(/\(.*/, ''),
        genomic_unit_type: isGeneAnnotation ? 'gene' : 'hgvs_variant',
        section: updatedSectionName,
      };

      const updatedAnalysis = await Annotations.attachAnnotationImage(annotation, attachment.data);
      if(!this.annotations[updatedSectionName])
        this.annotations[updatedSectionName] = [{file_id: updatedAnalysis['image_id'], created_date: ''}];        
      else
        this.annotations[updatedSectionName].push({file_id: updatedAnalysis['image_id'], created_date: ''});
      
        console.log(this.annotations)
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

.sections {
  flex: 7 1 auto;
}

.sidebar {
  position: sticky;
}

</style>
