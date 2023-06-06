<template>
  <a :href="value" target="_blank" rel="noreferrer noopener" class="linkout">
    <img :src="linkoutImageSrc(imageFilename)" :alt="altText" :style="linkoutStyle" />
  </a>
</template>

<script>
export default {
  name: 'icon-linkout-dataset',
  props: {
    value: {
      type: String,
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
  computed: {
    linkoutStyle: function() {
      if (typeof(this.value) == 'undefined') {
        return {
          opacity: 0.25,
        };
      }
      return {
        opacity: 1,
      };
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

.linkout {
  background-color: var(--rosalution-white);
  overflow:hidden;
}

.linkout img {
  max-height: 1.5rem;
  padding-right: var(--p-10)
}

</style>
