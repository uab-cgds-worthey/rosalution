<template>
  <div class="dataset-container">
    <DatasetLabel :label="label" :datasetValue="value"></DatasetLabel>
    <span v-if="!availableData" class="set-section dataset-bar dataset-bar-fill-unavailable" data-test="dataset-bar">
    </span>
    <span v-else class="set-section dataset-bar" data-test="dataset-bar">
      <span v-for="item in setItems" :key=item.key :style=item.style class="set-text">
        {{ item.content }}
      </span>
    </span>
  </div>
</template>

<script setup>
import DatasetLabel from '@/components/AnnotationView/DatasetLabel.vue';

import {isDatasetAvailable, useSetBarCalculations} from '@/components/AnnotationView/datasetRenderingUtility.js';

const props = defineProps({
  label: {
    type: String,
  },
  value: {
    type: String,
  },
  set: {
    type: Array,
    default: () => {
      return [];
    },
  },
  ticker: {
    type: Boolean,
    default: false,
  },
});

const availableData = isDatasetAvailable(props.value);
const setItems = useSetBarCalculations(props.value, props.set);

</script>
