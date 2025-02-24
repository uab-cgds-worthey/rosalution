<template>
  <div class="dataset-container">
    <DatasetLabel :label="label" :datasetValue="value" class="dataset-label-flex-parent-style"></DatasetLabel>
    <span class="highlight-text" :style="highlightStyle">{{ value }}</span>
  </div>
</template>

<script setup>

import DatasetLabel from '@/components/AnnotationView/DatasetLabel.vue';

const props = defineProps({
  label: {
    type: String,
  },
  value: {
    type: String,
  },
  highlight: {
    type: Object,
    required: true,
  },
});

function calculateHighlightStyle() {
  const style = {
    'background-color': 'var(--rosalution-grey-300)',
  };

  if ( !(props.value in props.highlight) ) {
    return style;
  }

  const highlightColour = props.highlight[props.value];
  if (highlightColour === 'Red') {
    style['background-color'] = 'var(--rosalution-red-200)';
  } else if (highlightColour === 'Blue') {
    style['background-color'] = 'var(--rosalution-blue-200)';
  } else if (highlightColour === 'Yellow') {
    style['background-color'] = 'var(--rosalution-yellow-200)';
  } else if (highlightColour === 'Green') {
    style['background-color'] = 'var(--rosalution-green-200)';
  }
  return style;
}
const highlightStyle = calculateHighlightStyle();

</script>
