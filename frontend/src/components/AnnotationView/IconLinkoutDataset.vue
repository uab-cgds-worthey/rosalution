<template>
  <a :href="value" target="_blank" rel="noreferrer noopener" class="linkout" :class="linkoutStyle" >
    <img :src="likoutImageSrc" :alt="altText" :class="imageStyle"/>
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

const linkoutStyle = (typeof(props.value) == 'undefined') ? 'linkout-unavailable' : 'linkout-available';
const classIfSvg = props.imageFilename.includes('.svg') ? 'svg' : '';
const imageStyle = [linkoutStyle, classIfSvg].join(' ');

const likoutImageSrc = new URL(`/src/assets/${props.imageFilename}`, import.meta.url);
</script>
