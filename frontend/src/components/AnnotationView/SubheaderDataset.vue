<template>
  <div class="dataset-container">
    <a v-if="linkout" :href="linkout" class="dataset-text-subheader" target="_blank" rel="noreferrer noopener">
        {{ label }}
        <font-awesome-icon icon="up-right-from-square" size="2xs" />
    </a>
    <span v-else class="dataset-text-subheader" :style="{ color: dataAvailabilityColour }">{{ label }}</span>
  </div>
</template>

<script setup>
const props = defineProps({
  label: {
    type: String,
  },
  linkout: {
    type: String,
    required: false,
  },
  enabled: {
    type: Boolean,
    default: true,
  },
});

const dataAvailabilityColour =  props.enabled  ? 'black' : 'var(--annotation-dataset-unavailable)';
</script>
