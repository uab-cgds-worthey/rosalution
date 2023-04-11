<template>
  <RosalutionHeader :username="this.username" :titleText="this.titleText" :actions="this.actions">
    <a v-if="mondayLink" :href="mondayLink" target="_blank" class="logo-link" data-test="monday-link">
        <img src="/src/assets/monday-avatar-logo.svg" class="monday-icon"/>
    </a>
    <a v-if="phenotipsLink" :href="phenotipsLink" target="_blank" class="logo-link" data-test="phenotips-link">
          <img src="/src/assets/phenotips-favicon-96x96.png" class="phenotips-icon"/>
    </a>
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
    mondayLink: {
      type: String,
      default: '',
      required: false,
    },
    phenotipsLink: {
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
  padding: 0;
  transform: translate(0, 4px);
}

img {
  margin-left: var(--p-5);
  margin-right: var(--p-5);
}

.monday-icon {
  width: 1.875rem; /* 30px */
  height: 1.875rem; /* 30px */
}

.phenotips-icon {
  width: 1.25rem; /* 20px */
  height: 1.25rem; /* 20px */
}
</style>
