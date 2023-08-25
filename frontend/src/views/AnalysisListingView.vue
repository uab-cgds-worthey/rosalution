<template>
<div>
  <app-header>
    <AnalysisListingHeader
      :username="auth.getUsername()"
      v-model:searchText="searchText"
      @logout="this.onLogout"
    />
  </app-header>
  <app-content>
    <AnalysisCreateCard
      @click="this.importPhenotipsAnalysis"
      v-if="auth.hasWritePermissions()"
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
    />
  </app-content>
  <app-footer>
    <InputDialog data-test="phenotips-import-dialog"/>
    <NotificationDialog data-test="notification-dialog" />
    <AnalysisListingLegend @filtered-changed="filteredUpdated"/>
  </app-footer>
</div>
</template>

<script>
import Analyses from '@/models/analyses.js';
import AnalysisCard from '@/components/AnalysisListing/AnalysisCard.vue';
import AnalysisCreateCard from '@/components/AnalysisListing/AnalysisCreateCard.vue';
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
    async importPhenotipsAnalysis() {
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
        await Analyses.importPhenotipsAnalysis(importFile.data);
        await notificationDialog
            .title('Successful import')
            .alert('');
        await this.getListing();
      } catch (error) {
        await notificationDialog
            .title('Failed to import phenotips analysis')
            .alert(error);
      }
    },
    async onLogout() {
      this.$router.push({name: 'logout'});
    },
  },
};
</script>

<style scoped>

app-content {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
  padding: 1rem;
  height: 100%;
}

app-header {
  position: sticky;
  top:0px;
  z-index: 10;
}

app-footer {
  position: sticky;
  bottom:0px;
  z-index: 10;
  justify-content: center;
  align-items: center;
  align-self: stretch;
  flex-grow: 0;
  display: flex;
  height:44px;
}

</style>
