<template>
<app-header>
  <AnalysisListingHeader
    :username="auth.getUsername()"
    v-model:searchText="searchText"
    @logout="this.onLogout"
  />
</app-header>
<app-content>
  <div class="card-feed">
    <AnalysisCreateCard
      @click="this.importNewAnalysis"
      v-if="auth.hasWritePermissions()"
      class="first-card"
      data-test="create-card"
    />
    <AnalysisCard
      v-for="analysis in searchedAnalysisListing"
      :key="analysis.id"
      :name="analysis.name"
      :description="analysis.description"
      :genomic_units="analysis.genomic_units"
      :nominated_by="analysis.nominated_by"
      :latest_status="analysis.latest_status"
      :created_date="analysis.created_date"
      :last_modified_date="analysis.last_modified_date"
      :third_party_links="analysis.third_party_links"
      data-test="analysis-card"
    />
  </div>
</app-content>
<app-footer>
  <div class="center-legend"><AnalysisListingLegend @filtered-changed="filteredUpdated"/></div>
  <InputDialog data-test="phenotips-import-dialog"/>
  <NotificationDialog data-test="notification-dialog" />
  <RosalutionFooter />
</app-footer>
</template>

<script>
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

import {authStore} from '@/stores/authStore.js';

export default {
  name: 'analysis-listing-view',
  components: {
    AnalysisCard,
    AnalysisCreateCard,
    AnalysisListingHeader,
    AnalysisListingLegend,
    InputDialog,
    NotificationDialog,
    RosalutionFooter,
  },
  data: function() {
    return {
      auth: authStore,
      searchText: '',
      analysisList: [],
      filteredChanged: [],
    };
  },
  computed: {
    filteredAnalysisListing() {
      return this.analysisList.filter((analysis) => {
        return this.filteredChanged.length === 0 ||
          this.filteredChanged.includes(analysis.latest_status);
      });
    },
    searchedAnalysisListing() {
      const lowerCaseSearchText = this.searchText.toLowerCase();

      return this.searchText === '' ? this.filteredAnalysisListing : this.filteredAnalysisListing.filter((analysis) => {
        return [analysis.name,
          analysis.created_date,
          analysis.last_modified_date,
          analysis.nominated_by,
        ].some((content) => content.toLowerCase().includes(lowerCaseSearchText)) ||
          analysis.genomic_units.some((unit) => {
            return (unit.gene && unit.gene.toLowerCase().includes(lowerCaseSearchText)) ||
              (unit.transcripts &&
                unit.transcripts.some((transcript) => transcript.toLowerCase().includes(lowerCaseSearchText))) ||
              (unit.variants && unit.variants.some((variant) => variant.toLowerCase().includes(lowerCaseSearchText)));
          });
      });
    },
  },
  created() {
    this.getListing();
  },
  methods: {
    filteredUpdated(filteredChanged) {
      this.filteredChanged = filteredChanged;
    },
    async getListing() {
      this.analysisList.length = 0;
      const analyses = await Analyses.all();

      // TODO: Handle Unauthorized error
      // Right now this is how we're handling unauthorization errors
      // There needs to be a proper way to manage these errors, otherwise each function will
      // have their own error message
      if (analyses.error) {
        console.warn('Cannot retrieve Analyses. User is not authorized or token is expired.');
        return;
      }

      this.analysisList.push(...analyses);
    },
    async importNewAnalysis() {
      const includeComments = false;
      const includeIcon = 'phenotips';

      const importFile = await inputDialog
          .confirmText('Upload')
          .cancelText('Cancel')
          .message(`Rosalution is <span style="color: var(--rosalution-red-200)">not authorized to store any
             Protected Health Information (PHI).</span> Double check the *.json files before importing them to create
             a new analysis.`)
          .file(includeComments, includeIcon)
          .prompt('Temp for file upload');

      if (!importFile) {
        return;
      }

      try {
        await Analyses.importNewAnalysis(importFile.data);
        await notificationDialog
            .title('Successful import')
            .alert('');
        await this.getListing();
      } catch (error) {
        await notificationDialog
            .title('Failed to import analysis')
            .alert(error);
      }
    },
    async onLogout() {
      this.$router.push({name: 'logout'});
    },
  },
  async beforeMount() {
    document.title = 'rosalution';
  },
};
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
