<template class="dataset-container">
  <div class="dataset-container">
    <span v-if="label" class="dataset-label" data-test="text-label">{{ label }}:</span>
    <span v-if="!isDataUnavailable" data-test="text-value" >{{ value }}</span>
  </div>
</template>

<script>
export default {
  name: 'text-dataset',
  props: {
    label: {
      type: String,
    },
    value: {
      type: [String, Array],
    },
  },
  computed: {
    isDataUnavailable: function() {
      return this.value == '.' || this.value == 'null' || this.value == null;
    },
    dataAvailabilityColour: function() {
      return this.isDataUnavailable ? 'var(--rosalution-grey-300)' : 'var(--rosalution-black)';
    },
  },
};
</script>

<style>

.dataset-container {
  display: flex;
  padding: var(--p-1);
  line-height: 24px; /**temproary until I see how things look */
}

.dataset-label {
  flex: 0 0 125px;
  font-weight: 600;
  color: v-bind(dataAvailabilityColour)
};

</style>
