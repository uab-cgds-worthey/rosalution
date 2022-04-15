<template>
  <div>
      This page opens the analysis view for each cpam case
  </div>
</template>

<script>
import Analyses from '@/models/analyses.js';

export default {
  name: 'analysis-view',
  components: {
  },
  data: function() {
    return {
      analysisName: '',
      analysisData: [],
    };
  },
  computed: {
    searchedAnalysisData() {
      return false;
    },
  },
  created() {
    this.getAnalysis();
  },
  methods: {
    async getAnalysis() {
      this.analysisData.length = 0;
      this.analysisData.push(...await Analyses.getAnalysis());
    },
    setAnalysisName(name) {
      this.analysisName = name;
    },
  },
};
</script>

<style>

div {
  font-family: "Proxima Nova", sans-serif;
}

</style>
