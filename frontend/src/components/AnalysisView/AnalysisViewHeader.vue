<template>
  <RosalutionHeader :username="this.username" :titleText="this.titleText" :actions="this.actions">
    <div class="anchor-links">
      <a v-for="anchorLink in this.sectionAnchors"
        :href="this.toAnchorId(anchorLink)"
        :key="anchorLink"
        class="menu-button"
      >
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
  flex-wrap: wrap;
  justify-content: center;
  gap: var(--p-8)
}

img {
  margin-left: var(--p-5);
  margin-right: var(--p-5);
}

</style>
