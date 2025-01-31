<template class="dataset-container">
  <div class="dataset-container">
    <span v-if="label && !linkout" class="dataset-label" data-test="text-label">{{ label }}</span>
    <a v-else-if="label && linkout" :href="linkout"
      class="dataset-label" data-test="text-label"
      target="_blank" rel="noreferrer noopener"
    >
      {{ label }}
      <font-awesome-icon icon="up-right-from-square" size="2xs"/>
    </a>
    <span v-if="!isDataUnavailable" class="text-value" data-test="text-value" >{{ content }}</span>
  </div>
</template>

<script>
export default {
  name: 'text-dataset',
  props: {
    label: {
      type: String,
    },
    linkout: {
      type: String,
      required: false,
    },
    value: {
      type: [String, Array],
    },
    delimeter: {
      type: String,
      default: ';   ',
    },
  },
  computed: {
    isDataUnavailable: function() {
      return this.value == '.' || this.value == 'null' || this.value == null || this.value == '';
    },
    dataAvailabilityColour: function() {
      return this.isDataUnavailable ?
        'var(--rosalution-grey-300)' :
          this.linkout ? 'var(--rosalution-purple-300)' :
          'var(--rosalution-black)';
    },
    content: function() {
      if (typeof(this.value) == 'object') {
        return this.value.join(this.delimeter);
      }

      return this.value;
    },
  },
};
</script>

<style scoped>

.dataset-label {
  color: v-bind(dataAvailabilityColour);
}

</style>
