<template>
    <div class="dataset-container">
      <DatasetLabel :label="label" :linkout="linkout" :datasetValue="value" style="font-size: 1.25rem;"></DatasetLabel>
    </div>
</template>

<script setup>
import DatasetLabel from '@/components/AnnotationView/DatasetLabel.vue';

defineProps({
  label: {
    type: String,
  },
  linkout: {
    type: String,
    required: false,
  },
  value: {
    type: [String, Array],
    default: () => {
      return [];
    },
  },
});
</script>
