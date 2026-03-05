<template>
  <aside>
    <router-link
      v-for="(anchor,index) in this.sectionAnchors"
      :to="{hash: `#${anchor}` }"
      :key="`${anchor}-${index}`"
      class="menu-button"
      @click.prevent=""
    >
      {{ toAnchorText(anchor) }}
    </router-link>
  </aside>
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
  aside {
    display: flex;
    flex-direction: column;
    background-color: var(--rosalution-white);
    border-radius: var(--content-border-radius);
    padding: var(--p-8);
    gap: var(--p-8);
    overflow-x: hidden;
  }
</style>
