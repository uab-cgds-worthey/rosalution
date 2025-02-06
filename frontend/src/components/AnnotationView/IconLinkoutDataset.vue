<template>
  <a :href="value" target="_blank" rel="noreferrer noopener" class="linkout">
    <img :src="likoutImageSrc" :alt="altText" :style="linkoutStyle" />
  </a>
</template>

<script setup>
const props = defineProps({
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
  });

  const linkoutStyle = (typeof(props.value) == 'undefined') ? { opacity: 0.25 } : { opacity: 1 };
  const likoutImageSrc = new URL(`/src/assets/${props.imageFilename}`, import.meta.url);
</script>
