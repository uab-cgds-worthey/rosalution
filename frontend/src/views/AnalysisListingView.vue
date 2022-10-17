<template>
<div>
  <app-header>
    <AnalysisListingHeader
      :username="username"
      v-on:search="onSearch"
      @logout="this.onLogout"
    />
  </app-header>
  <app-content>
    <AnalysisCreateCard
      @click="this.importPhenotipsAnalysis"
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
    />
  </app-content>
  <app-footer>
    <InputDialog data-test="phenotips-import-dialog"/>
    <NotificationDialog data-test="notification-dialog" />
    <AnalysisListingLegend/>
  </app-footer>
</div>
</template>

<script>
import Analyses from '@/models/analyses.js';
import AnalysisCard from '@/components/AnalysisListing/AnalysisCard.vue';
import AnalysisCreateCard from '@/components/AnalysisListing/AnalysisCreateCard.vue';
import AnalysisListingHeader from '@/components/AnalysisListing/AnalysisListingHeader.vue';
import AnalysisListingLegend from '@/components/AnalysisListing/AnalysisListingLegend.vue';
import Auth from '../models/authentication.js';

import InputDialog from '../components/Dialogs/InputDialog.vue';
import NotificationDialog from '@/components/Dialogs/NotificationDialog.vue';

import inputDialog from '@/inputDialog.js';
import notificationDialog from '@/notificationDialog.js';

import { userStore } from '@/stores/authStore.js';

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
      store: userStore,
      searchQuery: '',
      analysisList: [],
      username: '',
    };
  },
  computed: {
    searchedAnalysisListing() {
      return this.searchQuery === '' ? this.analysisList : this.analysisList.filter( (analysis) => {
        return analysis.name.includes(this.searchQuery) ||
          analysis.genomic_units.some((unit) => {
            if (unit.gene !== undefined) {
              return unit.gene.includes(this.searchQuery);
            } else if ( unit.transcript !== undefined ) {
              return unit.transcript.includes(this.searchQuery);
            }
            return false;
          });
      });
    },
  },
  created() {
    this.getListing();
  },
  computed: {
    username() {
      return this.store.state.name;
    }
  },
  methods: {
    async getListing() {
      this.analysisList.length = 0;
      const analyses = await Analyses.all();

      // TODO: Handle Unauthorized error
      // Right now this is how we're handling unauthorization errors
      // There needs to be a proper way to user09e these errors, otherwise each function will
      // have their own error message
      if (analyses.error) {
        console.warn('Cannot retrieve Analyses. User is not authorized or token is expired.');
        return;
      }

      this.analysisList.push(...analyses);
    },
    onSearch(query) {
      this.searchQuery = query;
    },
    async importPhenotipsAnalysis() {
      const includeComments = false;
      const includeIcon = 'phenotips';

      const importFile = await inputDialog
          .confirmText('Upload')
          .cancelText('Cancel')
          .file(includeComments, includeIcon)
          .prompt('Temp for file upload');

      if (!importFile) {
        return;
      }

      try {
        await Analyses.importPhenotipsAnalysis(importFile.data);
        await notificationDialog
            .title('Successful import')
            .alert('Imported Phenotips Case successfully!');
      } catch (error) {
        await notificationDialog
            .title('Failed to import phenotips analysis')
            .alert(error);
      }
    },
    async onLogout() {
      await Auth.logout();
      this.$router.push({path: '/rosalution/login'});
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
