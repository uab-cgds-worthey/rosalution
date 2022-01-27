<template>
  
  <content>
  Listing of Analyses
  </content>
</template>

<script>
import Analyses from '@/models/analyses.js';

export default {
  name: 'analysis-listing',
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
