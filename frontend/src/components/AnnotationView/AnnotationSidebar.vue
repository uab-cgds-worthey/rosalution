<template>
  <div>
    <a v-for="(anchor,index) in this.sectionAnchors" :href="`#${anchor}`" :key="`${anchor}-${index}`">
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
  margin-top: var(--p-10);
  margin-left: var(--p-10);
  margin-bottom: var(--p-10);
  overflow-x: hidden;
  max-height: 100vh;
  width: fit-content;
}

div a {
  border-radius: var(--content-border-radius);
  background-color: var(--primary-background-color);
  color: var(--rosalution-purple-200);
  padding: var(--p-5);
  margin: var(--p-5);
  font-size: 1.125rem; /* 18px */
  font-weight: 700;
  width: fit-content;
}

/*
div h2 {
  margin: 0;
  flex: 2 1 auto;
} */
</style>
