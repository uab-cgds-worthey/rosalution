<template>
  <div class="analysis-view">
    <app-header>
      </app-header>
      <app-content>
        <GeneBox
          v-for="genomicUnit in genomicUnitsList"
          :key="genomicUnit.id"
          :name="this.analysis_name"
          :gene="genomicUnit.gene"
          :transcripts="genomicUnit.transcripts"
          :variants="genomicUnit.variants"
        />
        <SectionBox
          v-for="section in sectionsList"
          :key="section.id"
          :header="section.header"
          :contentList="section.content"
        />
        <SupplementalFormList/>
      </app-content>
  </div>
</template>

<script>
import Analyses from '@/models/analyses.js';
import SectionBox from '../components/AnalysisView/SectionBox.vue';
import GeneBox from '../components/AnalysisView/GeneBox.vue';
import SupplementalFormList from '../components/AnalysisView/SupplementalFormList.vue';

export default {
  name: 'analysis-view',
  components: {
    SectionBox,
    GeneBox,
    SupplementalFormList,
  },
  props: ['analysis_name'],
  data: function() {
    return {
      analysis: {},
      sectionsList: [],
      genomicUnitsList: [],
    };
  },
  created() {
    this.getAnalysis();
  },
  methods: {
    async getAnalysis() {
      this.analysis = {...await Analyses.getAnalysis(this.analysis_name)};
      this.getSections();
      this.getGenomicUnits();
    },
    getSections() {
      this.sectionsList=this.analysis.sections;
    },
    getGenomicUnits() {
      this.genomicUnitsList=this.analysis.genomic_units;
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
