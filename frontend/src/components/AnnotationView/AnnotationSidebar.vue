<template>
  <div>
    <a v-for="(anchor,index) in this.sectionAnchors"
      :href="`#${anchor}`"
      :key="`${anchor}-${index}`"
      class="menu-button"
    >
      {{ toAnchorText(anchor) }}
    </a>
  </div>
</template>

<script>
export default {
  name: 'annotation-sidebar',
  props: {
    sectionAnchors: Array,
  },
  methods: {
    toAnchorText(anchor) {
      return `${anchor.replace(/_/g, ' ')}`;
    },
  },
};
</script>

<style scoped>
  div {
    display: inline-flex;
    flex-direction: column;
    justify-content: flex-start;
    background-color: var(--rosalution-white);
    border-radius: var(--content-border-radius);
    padding: var(--p-8);
    gap: var(--p-8);
    margin-top: var(--p-10);
    overflow-x: hidden;
  }
</style>
