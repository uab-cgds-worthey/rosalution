<template>
  <a :href="value" target="_blank" ref="noreferrer noopener">
    <img :src="linkoutImageSrc(imageFilename)" :alt="altText" />
  </a>
</template>

<script>
export default {
  name: 'icon-linkout-dataset',
  props: {
    value: {
      type: String,
      required: true,
    },
    altText: {
      type: String,
      required: true,
    },
    imageFilename: {
      type: String,
      required: true,
    },
  },
  methods: {
    linkoutImageSrc(imageFilename) {
      return new URL(`/src/assets/${imageFilename}`, import.meta.url);
    },
  },
};
</script>

<style scoped>

a img {
  height:100%;
  margin-right: var(--p-10)
}

</style>
