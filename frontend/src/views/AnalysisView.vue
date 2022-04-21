<template>
  <div>
    <app-header>
      This page opens the analysis view for each cpam case: Data for <p data-test="analysis-name">{{analysis_name}}</p>
      </app-header>
      <app-content>
        <p>{{ analysis }}</p>
      </app-content>
  </div>
</template>

<script>
import Analyses from '@/models/analyses.js';

export default {
  name: 'analysis-view',
  components: {
  },
  props: ['analysis_name'],
  data: function() {
    return {
      analysis: {},
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
      this.analysis = {...await Analyses.getAnalysis(this.analysis_name)};
    },
  },
};
</script>

<style>

div {
  font-family: "Proxima Nova", sans-serif;
}

</style>
