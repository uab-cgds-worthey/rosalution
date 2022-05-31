<template>
  <div class="analysis-view">
    <app-header>
      This page opens the analysis view for each cpam case: Data for {{analysis_name}}
      </app-header>
      <app-content>
        <GeneBox/>
        <SectionBox
          v-for="section in sectionsList"
          :key="section.id"
          :header="section.header"
          :contentList="section.content"
        />
      </app-content>
  </div>
</template>

<script>
import Analyses from '@/models/analyses.js';
import SectionBox from '../components/AnalysisView/SectionBox.vue';
import GeneBox from '../components/AnalysisView/GeneBox.vue';

export default {
  name: 'analysis-view',
  components: {
    SectionBox,
    GeneBox,
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
      this.getSections();
    },
    getSections() {
      this.sectionsList=this.analysis.sections;
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
