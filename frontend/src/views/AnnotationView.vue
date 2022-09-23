<template>
  <app-header>
    <AnnotationViewHeader :titleText="this.analysis_name" :genes="[this.gene]" :variants="[this.variant]">
    </AnnotationViewHeader>
  </app-header>
  <app-content>
    <AnnotationSection
      v-for="(section, index) in this.rendering" :key="`${section.type}-${index}`"
      :header="this[section.header] ? this[section.header] : section.header"
    >
    </AnnotationSection>
  </app-content>
</template>

<script>
import Analyses from '@/models/analyses.js';
import Auth from '@/models/authentication.js';

import AnnotationSection from '@/components/AnnotationView/AnnotationSection.vue';
import AnnotationViewHeader from '@/components/AnnotationView/AnnotationViewHeader.vue';

export default {
  name: 'annotation-view',
  components: {
    AnnotationSection,
    AnnotationViewHeader,
  },
  props: ['analysis_name', 'gene', 'variant'],
  data: function() {
    return {
      rendering: [],
      username: '',
    };
  },
  created() {
    this.getUsername();
    this.getRenderingConfiguration();
  },
  methods: {
    async getUsername() {
      const fetchUser = await Auth.getUser();
      console.log(fetchUser);
      this.username = fetchUser['username'];
    },
    async getRenderingConfiguration() {
      this.rendering.push(...await Analyses.getAnnotationConfiguration(this.analysis_name));
    },
  },
};
</script>

<style scoped>

</style>
