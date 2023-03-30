<template>
  <RosalutionHeader :username="this.username" :titleText="this.titleText" :actions="this.actions">
    <a v-if="mondayLink" :href="mondayLink" class="logo-link">
        <img src="/src/assets/monday-avatar-logo.svg"/>
    </a>
    <!-- Add a similar block for Phenotips logo when needed -->
    <div>
      <a v-for="anchorLink in this.sectionAnchors" :href="this.toAnchorId(anchorLink)" :key="anchorLink">
        {{ anchorLink }}
      </a>
    </div>
  </RosalutionHeader>
</template>

<script>
import RosalutionHeader from '@/components/RosalutionHeader.vue';

export default {
  name: 'analysis-view-header-component',
  components: {
    RosalutionHeader,
  },
  props: {
    username: {
      type: String,
      default: undefined,
      required: false,
    },
    titleText: {
      type: String,
      required: true,
    },
    sectionAnchors: {
      type: Array,
      required: true,
    },
    actions: {
      type: Array,
      required: true,
    },
    monday_com: {
      type: String,
      default: '',
      required: false,
    },
    phenotips_com: {
      type: String,
      default: '',
      required: false,
    },
  },
  methods: {
    toAnchorId(anchorText) {
      return `#${anchorText.replace(' ', '_')}`;
    },
  },
  computed: {
    mondayLink() {
      return this.monday_com;
    },
  },
};
</script>

<style scoped>

div {
  flex: 1 1 auto;
  display: inline-flex;
  justify-content: center;
}

div a {
  border-radius: var(--content-border-radius);
  background-color: var(--primary-background-color);
  color: var(--rosalution-purple-200);
  padding: var(--p-5);
  margin-left: var(--p-5);
  margin-right: var(--p-5);
  font-size: 1.125rem; /* 18px */
  font-weight: 700;
}

.logo-link {
  background-color: transparent;
}

img {
  height: 24px;
  width: 24px;
  margin-left: var(--p-5);
  margin-right: var(--p-5);
}
</style>
