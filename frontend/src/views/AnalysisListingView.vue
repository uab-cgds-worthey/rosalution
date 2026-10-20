<template>
<app-header>
  <AnalysisListingHeader
    :username="username"
    v-model:searchText="searchText"
    @logout="logout"
  />
</app-header>
<app-content>
  <div class="card-feed" v-if="isLoaded">
    <AnalysisCreateCard
      @click="importNewAnalysis"
      v-if="hasWritePermissions"
      class="first-card"
      data-test="create-card"
    />
    <AnalysisCard
      v-for="analysis in renderedAnalysisList"
      :key="analysis.id"
      :name="analysis.name"
      :description="analysis.description"
      :genomic_units="analysis.genomic_units"
      :nominated_by="analysis.nominated_by"
      :project_name="analysis.project_name"
      :latest_status="analysis.latest_status"
      :created_date="analysis.created_date"
      :last_modified_date="analysis.last_modified_date"
      :third_party_links="analysis.third_party_links"
      data-test="analysis-card"
    />
  </div>
</app-content>
<app-footer>
  <div class="center-legend"><AnalysisListingLegend  v-if="isLoaded"  @filtered-changed="filteredStatusUpdate"/></div>
  <InputDialog data-test="phenotips-import-dialog"/>
  <NotificationDialog data-test="notification-dialog" />
  <RosalutionFooter />
</app-footer>
</template>

<script setup>
import {onMounted, ref, computed, shallowRef, watch} from 'vue';

import Analyses from '@/models/analyses.js';
import AnalysisCard from '@/components/AnalysisListing/AnalysisCard.vue';
import AnalysisCreateCard from '@/components/AnalysisListing/AnalysisCreateCard.vue';
import RosalutionFooter from '@/components/RosalutionFooter.vue';
import AnalysisListingHeader from '@/components/AnalysisListing/AnalysisListingHeader.vue';
import AnalysisListingLegend from '@/components/AnalysisListing/AnalysisListingLegend.vue';

import InputDialog from '@/components/Dialogs/InputDialog.vue';
import NotificationDialog from '@/components/Dialogs/NotificationDialog.vue';

import inputDialog from '@/inputDialog.js';
import notificationDialog from '@/notificationDialog.js';

import {useAuth} from '@/composables/useAuth.js';

const {username, hasWritePermissions, logout} = useAuth();

const analysisList = shallowRef([]);
const renderedAnalysisList = ref([]);

const projects = ref([]);

const searchText = ref('');
const workflowStatusFilters = ref([]);

const isLoaded = ref(false);

const workflowFilteredAnalysisList = computed(() => {
  // console.log("COMPUTED-workflowFilteredAnalysisList ---")
  return analysisList.value.filter((analysis) => {
    return workflowStatusFilters.value.length === 0 || workflowStatusFilters.value.includes(analysis.latest_status);
  });
});

const searchedAnalysisListing = computed(() => {
  const lowerCaseSearchText = searchText.value.toLowerCase();
  const hasSearchText = searchText.value === '';

  if ( hasSearchText ) {
    return workflowFilteredAnalysisList.value;
  }
  const filteredList = workflowFilteredAnalysisList.value.filter((analysis) => {
    const analysisContent = [analysis.name,
      analysis.created_date,
      analysis.last_modified_date,
      analysis.nominated_by,
      analysis.project_name,
    ];

    const wasFound = analysisContent.some((content) => {
      const individualFound = content.toLowerCase().includes(lowerCaseSearchText) ||
        analysis.genomic_units.some((unit) => {
          return (unit.gene && unit.gene.toLowerCase().includes(lowerCaseSearchText)) ||
            (unit.transcripts &&
              unit.transcripts.some((transcript) => transcript.toLowerCase().includes(lowerCaseSearchText))) ||
            (unit.variants && unit.variants.some((variant) => variant.toLowerCase().includes(lowerCaseSearchText)));
        });
      return individualFound;
    });
    return wasFound;
  });

  return filteredList;
});

const RENDER_LISTING_BATCH_SIZE = 5;
const renderNextBatch = () => {
  const currentLength = renderedAnalysisList.value.length;
  // console.log('RENDER NEXT BATCH--- next batch ', currentLength);
  if (currentLength < searchedAnalysisListing.value.length) {
    const nextBatch = searchedAnalysisListing.value.slice(currentLength, currentLength + RENDER_LISTING_BATCH_SIZE);
    renderedAnalysisList.value.push(...nextBatch);
    // console.log('RENDER NEXT BATCH--- next pushed done ', renderedAnalysisList.value.length);
    renderNextBatch();
  }
  // console.log('searched analyses next complete ', searchedAnalysisListing.value.length);
};

watch(searchedAnalysisListing, () => {
  renderedAnalysisList.value = [];
});

watch([workflowFilteredAnalysisList, renderedAnalysisList, searchedAnalysisListing, searchText], () => {
  // console.log("WATCHER-Calling RenderNextBatch ---");
  renderNextBatch();
  // console.log("WATCHER-Calling RenderNextBatch --- DONE");
}, {flush: 'post'});

const projectsAvailable = computed(() => {
  return projects.value.map((project) => {
    return {
      'value': project._id,
      'text': project.name,
    };
  });
});

function filteredStatusUpdate(newFilteredStatus) {
  workflowStatusFilters.value = newFilteredStatus;
}

Analyses.getProjects().then((data) => {
  projects.value.length = 0;
  projects.value.push(...data);
});

async function getListing() {
  Analyses.all().then((data)=> {
    // TODO: Handle Unauthorized error
    // Right now this is how we're handling unauthorization errors
    // There needs to be a proper way to manage these errors, otherwise each function will
    // have their own error message
    if (data.error) {
      console.warn('Cannot retrieve Analyses. User is not authorized or token is expired.');
      return;
    }
    analysisList.value = data;
    isLoaded.value = true;
  });
};

getListing();

async function importNewAnalysis() {
  const includeComments = false;
  const includeIcon = 'phenotips';
  const fileTypesAccept = '.json';

  const includeProjects = {
    selected: '',
    options: projectsAvailable.value,
  };

  const importFile = await inputDialog
      .confirmText('Upload')
      .cancelText('Cancel')
      .message(`Rosalution is <span style="color: var(--rosalution-red-200)">not authorized to store any
          Protected Health Information (PHI).</span> Double check the *.json files before importing them to create
          a new analysis.`)
      .file(includeComments, includeIcon, fileTypesAccept, includeProjects)
      .prompt('Temp for file upload');

  if (!importFile) {
    return;
  }

  if ( '' == importFile.data ) {
    await notificationDialog.title('Missing Analysis Json')
        .alert('An uploaded analysis json is required to import an analysis.');
    return;
  }

  if ( '' == importFile.projectSelect.selected) {
    await notificationDialog.title('Missing Selected Project')
        .alert('A Rosalution project must be selected to proceed with the import.');
    return;
  }

  const selectedProject = projectsAvailable.value.find((project) => project.value == importFile.projectSelect.selected);

  const confirmedImport = await notificationDialog
      .title(`Confirm Analysis Import into Project '${selectedProject.text}'`)
      .confirmText('Confirm')
      .cancelText('Cancel')
      .confirm(
          `This will import the uploaded json '${importFile.name}' into the ${selectedProject.text} project.`,
      );

  if (!confirmedImport) {
    return;
  }

  try {
    await Analyses.importNewAnalysis(importFile.projectSelect.selected, importFile.data);
    await notificationDialog
        .title('Successful import')
        .alert('');
    await getListing();
  } catch (error) {
    await notificationDialog
        .title('Failed to import analysis')
        .alert(error);
  }
}

document.title = 'rosalution';

onMounted(async () => {
  // console.log("FROM ON MOUNTED: ")
  renderNextBatch();
  // console.log("FROM ON MOUNTED: done")
});

</script>

<style scoped>

app-content {
  display: contents;

  --max-card-width: 11.25rem;
  --card-height: 18.125rem;
  --card-border-radius: 1.25rem;
}


app-header {
  position: sticky;

  top:0px;
  z-index: 10;
}

app-footer {
  position: sticky;
  bottom:1.25rem;
  z-index: 10;

  display: flex;
  justify-content: center;
  flex-direction: column;
}

.center-legend {
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-feed {
  grid-row: 2 / -2;
  grid-column: 1 / -1;

  display: grid;
  grid-template-columns: repeat(auto-fill, var(--max-card-width));
  grid-template-rows: repeat(auto-fill, var(--card-height));
  justify-content: center;

  gap: var(--p-8);
}

.first-card {
  grid-row: 1 / 2;
  grid-column: 1 / 2;
}

:deep(.analysis-card:hover) {
  box-shadow: 0 0.5em 0.5em -0.4em;
  transform: translateY(-0.4em);
}

:deep(.analysis-card:active) {
  transform: translateY(0em);
  transition: all .1s ease-in-out;
}

:deep(.analysis-card) {
  height: var(--card-height);

  display: flex;
  flex-direction: column;
  gap: var(--p-05);

  box-sizing: border-box;

  padding: var(--p-8) var(--p-5) var(--p-8) var(--p-5);

  border-radius: var(--card-border-radius);
  border: solid 0.625rem;
  background-color: var(--rosalution-white);

  transition: all .2s ease-in-out;

  text-decoration: none;
}

</style>
