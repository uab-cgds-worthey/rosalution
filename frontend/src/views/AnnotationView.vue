<template>
  <app-header>
    <AnnotationViewHeader :titleText="this.analysis_name" :genes="[this.gene]" :variants="[this.variant]">
    </AnnotationViewHeader>
  </app-header>
  <app-content>
    <div class="sections">
      <AnnotationSection
        v-for="(section, index) in this.rendering" :key="`${section.type}-${section.anchor}-${index}`"
        :header="sectionHeader(section.header)"
        :id="`${section.anchor}`"
      >
      </AnnotationSection>
    </div>
    <AnnotationSidebar class="sidebar" :section-anchors="sectionAnchors"></AnnotationSidebar>
  </app-content>
</template>

<script>
import Analyses from '@/models/analyses.js';
import Annotations from '@/models/annotations.js';
import Auth from '@/models/authentication.js';

import AnnotationSection from '@/components/AnnotationView/AnnotationSection.vue';
import AnnotationSidebar from '@/components/AnnotationView/AnnotationSidebar.vue';
import AnnotationViewHeader from '@/components/AnnotationView/AnnotationViewHeader.vue';

export default {
  name: 'annotation-view',
  components: {
    AnnotationSection,
    AnnotationSidebar,
    AnnotationViewHeader,
  },
  props: ['analysis_name', 'gene', 'variant'],
  data: function() {
    return {
      rendering: [],
      username: '',
      annotations: {},
    };
  },
  computed: {
    sectionAnchors() {
      return this.rendering.map((section) => {
        return section.anchor;
      });
    },
  },
  created() {
    this.getUsername();
    this.getRenderingConfiguration();
    this.getAnnotations();
  },
  methods: {
    sectionHeader(header) {
      return header in this ? this[header] : header;
    },
    async getUsername() {
      const fetchUser = await Auth.getUser();
      this.username = fetchUser['username'];
    },
    async getRenderingConfiguration() {
      this.rendering.push(...await Analyses.getAnnotationConfiguration(this.analysis_name));
    },
    async getAnnotations() {
      this.annotations = {...await Annotations.getAnnotations(this.analysis_name, this.gene, this.variant)};
    },
  },
};
</script>

<style scoped>

app-content {
  display: flex;
  flex-direction: row;
  gap: var(--p-10);
}

.sections {
  flex: 7 1 auto;
}

.sidebar {
  position: sticky;
}

</style>
