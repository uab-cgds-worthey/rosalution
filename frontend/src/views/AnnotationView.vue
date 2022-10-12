<template>
  <app-header>
    <AnnotationViewHeader :analysisName="this.analysis_name" :genes="[this.gene]" :variants="[this.variant]">
    </AnnotationViewHeader>
  </app-header>
  <app-content>
    <div class="sections">
      <AnnotationSection
        v-for="(section, index) in this.rendering" :key="`${section.type}-${section.anchor}-${index}`"
        :header="sectionHeader(section.header)" v-bind="section.props"
        :id="`${section.anchor}`"
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
                v-bind="datasetConfig.props"
                :linkout="linkoutUrl(datasetConfig)"
                :value="annotations[datasetConfig.dataset]"
                :data-test="datasetConfig.dataset"
              />
          </div>
        </template>
      </AnnotationSection>
    </div>
    <AnnotationSidebar class="sidebar" :section-anchors="sectionAnchors"></AnnotationSidebar>
  </app-content>
</template>

<script>
import Analyses from '@/models/analyses.js';
import Annotations from '@/models/annotations.js';
import Auth from '@/models/authentication.js';

import AnnotationSection from '@/components/AnnotationView/AnnotationSection.vue';
import AnnotationSidebar from '@/components/AnnotationView/AnnotationSidebar.vue';
import AnnotationViewHeader from '@/components/AnnotationView/AnnotationViewHeader.vue';

import ClinvarDataset from '@/components/AnnotationView/ClinvarDataset.vue';
import IconLinkoutDataset from '@/components/AnnotationView/IconLinkoutDataset.vue';
import ScoreDataset from '@/components/AnnotationView/ScoreDataset.vue';
import TextDataset from '@/components/AnnotationView/TextDataset.vue';
import TranscriptDatasets from '@/components/AnnotationView/TranscriptDatasets.vue';

export default {
  name: 'annotation-view',
  components: {
    AnnotationSection,
    AnnotationSidebar,
    AnnotationViewHeader,
    ClinvarDataset,
    IconLinkoutDataset,
    ScoreDataset,
    TextDataset,
    TranscriptDatasets,
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
      rendering: [],
      username: '',
      annotations: {},
    };
  },
  computed: {
    sectionAnchors() {
      return this.rendering.map((section) => {
        return section.anchor;
      });
    },
  },
  created() {
    this.getUsername();
    this.getRenderingConfiguration();
    this.getAnnotations();
  },
  methods: {
    sectionHeader(header) {
      return header in this ? this[header] : header;
    },
    linkoutUrl(datasetConfig) {
      return 'linkout_dataset' in datasetConfig ? this.annotations[datasetConfig['linkout_dataset']] : undefined;
    },
    async getUsername() {
      const fetchUser = await Auth.getUser();
      this.username = fetchUser['username'];
    },
    async getRenderingConfiguration() {
      this.rendering.push(...await Analyses.getAnnotationConfiguration(this.analysis_name));
    },
    async getAnnotations() {
      this.annotations = {...await Annotations.getAnnotations(this.analysis_name, this.gene, this.variant)};
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
