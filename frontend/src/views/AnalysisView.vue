<template>
  <div class="analysis-view">
    <app-header>
      This page opens the analysis view for each cpam case: Data for {{analysis_name}}
      </app-header>
      <app-content>
        <p>{{ analysis }}</p>
        <ContentBox/>
      </app-content>
  </div>
</template>

<script>
import Analyses from '@/models/analyses.js';
import ContentBox from '../components/AnalysisView/ContentBox.vue';

export default {
  name: 'analysis-view',
  components: {
    ContentBox,
  },
  props: ['analysis_name'],
  data: function() {
    return {
      analysis: {},
      sectionsList: [],
    };
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

app-content {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  height: 100%;
}

app-header {
  position: sticky;
  top:0px;
  z-index: 10;
}

</style>
