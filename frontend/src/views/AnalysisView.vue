<template>
  <div>
      <app-header>
        <AnalysisViewHeader
          :username="username"
          :actions="menuActions"
          :titleText="this.analysis_name"
          :sectionAnchors="this.sectionsHeaders"
          data-test="analysis-view-header">
        </AnalysisViewHeader>
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
          :id="section.header.replace(' ', '_')"
          :key="section.id"
          :header="section.header"
          :contentList="section.content"
        />
        <SupplementalFormList
          id="Supplemental_Attachments"
        />
      </app-content>
  </div>
</template>

<script>
import Analyses from '@/models/analyses.js';
import AnalysisViewHeader from '../components/AnalysisView/AnalysisViewHeader.vue';
import SectionBox from '../components/AnalysisView/SectionBox.vue';
import GeneBox from '../components/AnalysisView/GeneBox.vue';
import SupplementalFormList from '../components/AnalysisView/SupplementalFormList.vue';
import User from '../models/user';

export default {
  name: 'analysis-view',
  components: {
    AnalysisViewHeader,
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
      username: '',
      menuActions: ['Edit', '----', 'Attach', 'Attach Monday.com', 'Connect PhenoTips'],
    };
  },
  computed: {
    sectionsHeaders() {
      const sections = this.sectionsList.map((section) => {
        return section.header;
      });
      sections.push('Supplemental Attachments');
      return sections;
    },
  },
  created() {
    this.getUsername();
    this.getAnalysis();
  },
  methods: {
    async getUsername() {
      const fetchUser = await User.getUser();
      console.log(fetchUser);
      this.username = fetchUser['username'];
    },
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

<style scoped>

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
