<template>
    <span v-if="label && !linkout" class="dataset-label" :style="{ color: dataAvailabilityColour }">{{ label }}</span>
    <a v-else-if="label && linkout" :href="linkout" class="dataset-label" target="_blank" rel="noreferrer noopener">
      {{ label }}
      <font-awesome-icon icon="up-right-from-square" size="2xs" />
    </a>
</template>

<script setup>
import {isDatasetAvailable} from '@/components/AnnotationView/datasetRenderingUtility.js'
const props = defineProps({
  label: {
    type: String,
  }, linkout: {
    type: String,
    required: false,
  }, datasetValue: {
    required: false,
  },
});

const isAvailable = isDatasetAvailable(props.datasetValue);
const dataAvailabilityColour =  isAvailable ? "black" : ".dataset-label-unavailable"

</script>
