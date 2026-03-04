<template>
  <app-header>
    <AnnotationViewHeader
      :username="username"
      :workflow_status="summary.latest_status"
      :analysisName="analysis_name"
      :genes="genomicUnits['genes']"
      :variants="genomicUnits['variants']"
      :activeGenomicUnits="active"
      :third_party_links="summary.third_party_links"
      @changed="onActiveGenomicUnitsChanged"
      @logout="onLogout"
    >
    </AnnotationViewHeader>
  </app-header>
  <app-content v-if="renderReady">
    <div class="sections">
      <AnnotationSection
        v-for="(section, index) in rendering"
        :key="`${section.type}-${active.gene}-${active.variant}-${section.anchor}-${index}`"
        :header="sectionHeader(section.header)" v-bind="section.props"
        :id="`${section.anchor}`" @attach-image="attachAnnotationImage"
        :writePermissions="hasWritePermissions"
      >
        <template #headerDatasets>
          <component
              v-for="(headerDatasetConfig, index) in section.header_datasets"
              :key="`${headerDatasetConfig.dataset}-${active.gene}-${active.variant}-${index}`"
              :is="datasetComponents[headerDatasetConfig.type]"
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
                :is="datasetComponents[datasetConfig.type]"
                :dataSet="datasetConfig.dataset"
                :genomicType="datasetConfig.genomicType"
                v-bind="buildProps(datasetConfig)"
                :value="annotations[datasetConfig.dataset]"
                :data-test="datasetConfig.dataset"
                :writePermissions="hasWritePermissions"
                @update-annotation-image="updateAnnotationImage"
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
  <app-footer>
    <RosalutionFooter></RosalutionFooter>
  </app-footer>
</template>

<script setup>
import Analyses from '@/models/analyses.js';
import Annotations from '@/models/annotations.js';

import AnnotationSection from '@/components/AnnotationView/AnnotationSection.vue';
import AnnotationSidebar from '@/components/AnnotationView/AnnotationSidebar.vue';
import AnnotationViewHeader from '@/components/AnnotationView/AnnotationViewHeader.vue';

import CardDataset from '@/components/AnnotationView/CardDataset.vue';
import ClinvarDataset from '@/components/AnnotationView/ClinvarDataset.vue';
import IconLinkoutDataset from '@/components/AnnotationView/IconLinkoutDataset.vue';
import ImagesDataset from '@/components/AnnotationView/ImagesDataset.vue';
import RosalutionFooter from '@/components/RosalutionFooter.vue';
import ScoreDataset from '@/components/AnnotationView/ScoreDataset.vue';
import SetDataset from '@/components/AnnotationView/SetDataset.vue';
import SubheaderDataset from '@/components/AnnotationView/SubheaderDataset.vue';
import TextDataset from '@/components/AnnotationView/TextDataset.vue';
import TranscriptDatasets from '@/components/AnnotationView/TranscriptDatasets.vue';
import InputDialog from '@/components/Dialogs/InputDialog.vue';
import NotificationDialog from '@/components/Dialogs/NotificationDialog.vue';
import TagDataset from '@/components/AnnotationView/TagDataset.vue';

import inputDialog from '@/inputDialog.js';
import notificationDialog from '@/notificationDialog.js';

import {authStore} from '@/stores/authStore.js';
import {useRouter} from 'vue-router';
import {computed, onBeforeMount, reactive, watch} from 'vue';

const datasetComponents = {
  'text-dataset': TextDataset,
  'score-dataset': ScoreDataset,
  'images-dataset': ImagesDataset,
  'set-dataset': SetDataset,
  'transcript-datasets': TranscriptDatasets,
  'tag-dataset': TagDataset,
  'icon-linkout-dataset': IconLinkoutDataset,
  'clinvar-dataset': ClinvarDataset,
  'card-dataset': CardDataset,
  'subheader-dataset': SubheaderDataset,
};

const props = defineProps({
  analysis_name: {
    type: String,
    required: true,
  },
  gene: {
    type: String,
    required: false,
  },
  variant: {
    type: String,
    required: false,
  },
});

const router = useRouter();

const renderingLayout = reactive([]);

const rendering = computed(() => {
  return renderingLayout.filter((section) => {
    const conditions = {
      'gene': active.gene && active.gene != '',
      'variant': active.variant && active.variant != '',
      'protein': active.protein && active.protein != '',
    };
    if (section.header in conditions) {
      return conditions[section.header];
    }

    return true;
  });
});

const annotations = reactive({});
const active = reactive({
  'gene': ( props.gene && props.gene != '' ) ? props.gene : ( history.state.gene || '' ),
  'variant': ( props.variant && props.variant != '' ) ? props.variant : ( history.state.variant || '' ),
});
const genomicUnits = reactive({
  'genes': {},
  'variants': [],
});

const summary = reactive({sections: []});

const username = computed(() => {
  return authStore.getUsername();
});

const hasWritePermissions = computed(() => {
  return authStore.hasWritePermissions();
});

const renderReady = computed(() => {
  return !( Object.keys(annotations).length === 0 || rendering.value.length === 0 );
});

const sectionAnchors = computed(() => {
  return rendering.value.map((section) => {
    return section.anchor;
  });
});

const activeVariantWithRemovedProtein = computed(() => {
  return active.variant.replace(/\(.*/, '');
});

const pageTitle = computed(() => {
  const variantString = active.variant && ('| ' + active.variant);
  return `${props.analysis_name} | ${active.gene} ${variantString} | rosalution`;
});

watch(pageTitle, () => {
  document.title = pageTitle.value;
});

watch(annotations, () => {
  if ( 'uniprot_id' in annotations ) {
    active.protein = annotations['uniprot_id'];
  }
});

onBeforeMount( async ()=> {
  await getGenomicUnits();
  await getRenderingConfiguration();
  await getAnnotations();
  await getSummaryByName();
});

async function getSummaryByName() {
  Object.assign(summary, await Analyses.getSummaryByName(props.analysis_name));
};

function sectionHeader(header) {
  return header in active ? active[header] : header;
};

function buildProps(datasetConfig) {
  return {
    ...datasetConfig.props,
    ...(
        'extra_annotation' in datasetConfig ?
          {[datasetConfig.extra_annotation]: annotations[datasetConfig[datasetConfig.extra_annotation]]} : {}
    ),
  };
};

/**
 * Logs user out of Rosalution
 */
function onLogout() {
  router.push({name: 'logout'});
}

async function getGenomicUnits() {
  Object.assign(genomicUnits, {...await Analyses.getGenomicUnits(props.analysis_name)});
  if (active.gene === '') {
    const genes = Object.keys(genomicUnits['genes']);
    active.gene = genes[0];
    if (genomicUnits['genes'][active.gene].length !== 0) {
      active.variant = genomicUnits['genes'][active.gene][0];
    }
  }
};

async function getRenderingConfiguration() {
  renderingLayout.push(...await Analyses.getAnnotationConfiguration(props.analysis_name));
};

async function getAnnotations() {
  Object.assign(
      annotations,
      {
        ...await Annotations.getAnnotations(props.analysis_name, active.gene, activeVariantWithRemovedProtein.value),
      },
  );
};

async function onActiveGenomicUnitsChanged(genomicUnitsChanged) {
  Object.keys(annotations).forEach((key) => delete annotations[key]);
  active.gene = genomicUnitsChanged.gene;
  active.variant = genomicUnitsChanged.variant;
  await(getAnnotations());
};

async function attachAnnotationImage(dataSet, genomicUnitType) {
  const includeComments = false;
  const attachment = await inputDialog
      .confirmText('Attach')
      .cancelText('Cancel')
      .file(includeComments, 'file', '.png, .jpg, .jpeg, .bmp')
      .prompt();

  if (!attachment) {
    return;
  }

  const genomicUnit = genomicUnitType.includes('gene') ? active.gene : activeVariantWithRemovedProtein.value;

  const annotation = {
    genomic_unit_type: genomicUnitType,
    annotation_data: attachment.data,
  };

  try {
    const updatedAnnotation = await Annotations.attachAnnotationImage(genomicUnit, dataSet, annotation);

    if (!annotations[dataSet]) {
      annotations[dataSet] = [...updatedAnnotation];
    } else {
      annotations[dataSet].splice(0);
      annotations[dataSet].push(...updatedAnnotation);
    }
  } catch (error) {
    await notificationDialog
        .title('Failure')
        .confirmText('Ok')
        .alert(error);
  }
};

async function updateAnnotationImage(fileId, dataSet, genomicUnitType) {
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

  const genomicUnit = genomicUnitType.includes('gene') ? active.gene : active.variant.replace(/\(.*/, '');

  const annotation = {
    genomic_unit_type: genomicUnitType,
    annotation_data: attachment.data,
  };

  if ('DELETE' == attachment) {
    await removeAnnotationImage(genomicUnit, dataSet, fileId, annotation);
    return;
  }

  try {
    const updatedAnnotation = await Annotations.updateAnnotationImage(genomicUnit, dataSet, fileId, annotation);
    annotations[dataSet].splice(0);
    annotations[dataSet].push(...updatedAnnotation);
  } catch (error) {
    await notificationDialog
        .title('Failure')
        .confirmText('Ok')
        .alert(error);
  }
}

async function removeAnnotationImage(genomicUnit, dataSet, fileId, annotation) {
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

  annotations[dataSet] = annotations[dataSet].filter( (obj) => {
    return obj.file_id !== fileId;
  });
};

onBeforeMount(() => {
  document.title = pageTitle.value;
});

</script>

<style scoped>

app-content {
  display: flex;

  grid-column: 1 / -2;
}

app-header {
  position: sticky;
  top:0px;
  z-index: 10;

  border-bottom: 4px solid var(--primary-background-color);
}

.sidebar {
  grid-row: 2 / -2;
  grid-column: -2 / -1;
  position: sticky;
  height: 91vh;
  top: 4rem;
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
