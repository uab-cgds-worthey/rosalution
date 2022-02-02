<template>
  <!--Header-->
  <app-header>Header Box - Analysis Listing</app-header>
  <!--Content-->
  <app-content>Content Box - Analysis Listing</app-content>
</template>

<script>
import Analyses from '@/models/analyses.js';

export default {
  name: 'analysis-listing-view',
  components: {
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
