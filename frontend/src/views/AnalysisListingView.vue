<template>
<div>
  <!--Header-->
  <app-header>
    <AnalysisListingHeader v-bind:username="username" v-on:search="onSearch"/>
  </app-header>
  <!--Content-->
  <app-content>
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
    <AnalysisListingLegend/>
  </app-footer>
</div>
</template>

<script>
import Analyses from '@/models/analyses.js';
import AnalysisCard from '../components/AnalysisListing/AnalysisCard.vue';
import AnalysisListingHeader from '@/components/AnalysisListing/AnalysisListingHeader.vue';
import AnalysisListingLegend from '../components/AnalysisListing/AnalysisListingLegend.vue';

export default {
  name: 'analysis-listing-view',
  components: {
    AnalysisCard,
    AnalysisListingHeader,
    AnalysisListingLegend,
  },
  data: function() {
    return {
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
    this.getUsername();
    this.getListing();
  },
  methods: {
    async getUsername() {
      const validateUrl = '/divergen/api/get_user';
      const newURL = await fetch(validateUrl, {
        method: 'GET',
        mode: 'cors',
      });

      const response = await newURL.json();

      this.username = response['username'];
    },
    async getListing() {
      this.analysisList.length = 0;
      this.analysisList.push(...await Analyses.all());
    },
    onSearch(query) {
      this.searchQuery = query;
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
