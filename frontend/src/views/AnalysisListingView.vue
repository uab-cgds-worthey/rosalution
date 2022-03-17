<template>
  <!--Header-->
  <app-header>diverGen</app-header>
  <!--Content-->
  <app-content>
    <AnalysisCard
    v-for="analysis in this.analysisList"
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
</template>

<script>
import Analyses from '@/models/analyses.js';
import AnalysisCard from '../components/AnalysisListing/AnalysisCard.vue';

export default {
  name: 'analysis-listing-view',
  components: {
    AnalysisCard,
  },
  data: function() {
    return {
      analysisList: [],
    };
  },
  created() {
    this.getListing();
  },
  methods: {
    async getListing() {
      this.analysisList.length = 0;
      this.analysisList.push(...await Analyses.all());
    },
  },
};
</script>

<style scoped>

app-content {
  display: flex;
  flex-wrap: wrap;
}

</style>
