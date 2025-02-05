<template>
      <!-- <dt class="dataset-label dataset-label-position" ">
      {{ label }}
    </dt> -->
    <div class="dataset-container">
      <span v-if="label && !linkout" class="dataset-label" :style="{ color: dataAvailabilityColour }">{{ label }}</span>
      <a v-else-if="label && linkout" :href="linkout" class="dataset-label" target="_blank" rel="noreferrer noopener">
        {{ label }}
        <font-awesome-icon icon="up-right-from-square" size="2xs" />
      </a>
  </div>
</template>

<script setup>
import {isDatasetAvailable} from '@/components/AnnotationView/datasetRenderingUtility.js'
const props = defineProps({
  label: {
    type: String,
    default: '',
  }, linkout: {
    type: String,
    required: false,
  }, datasetValue: {
    type: [String, Array],
  },
});

const isAvailable = isDatasetAvailable(props.datasetValue);
const dataAvailabilityColour =  isAvailable ? "black" : ".dataset-label-unavailable"

// dataAvailabilityColour() {
//   return this.isDataUnavailable ?
//     'var(--rosalution-grey-300)' :
//     this.linkout ? 'var(--rosalution-purple-300)' :
//       'var(--rosalution-black)';
// }

</script>
