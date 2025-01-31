<template>
  <div class="dataset-container">
    <span v-if="label && !linkout" class="dataset-label">{{ label }}</span>
    <a v-else-if="label && linkout" :href="linkout" class="dataset-label" target="_blank" rel="noreferrer noopener">
      {{ label }}
      <font-awesome-icon icon="up-right-from-square" size="2xs" />
    </a>
    <div v-if="!isDataUnavailable" class="tags-container">
      <div class="tag" v-for="(item, index) in content" :key="index">
        {{ item }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'tag-dataset',
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
      default: '; ',
    },
  },
  computed: {
    isDataUnavailable() {
      return this.value == '.' || this.value == 'null' || this.value == null;
    },
    dataAvailabilityColour() {
      return this.isDataUnavailable ?
        'var(--rosalution-grey-300)' :
        this.linkout ? 'var(--rosalution-purple-300)' :
          'var(--rosalution-black)';
    },
    content() {
      if (typeof (this.value) == 'object') {
        return this.value;
      }

      return this.value.split(this.delimeter);
    },
  },
};
</script>

<style scoped>

.dataset-label {
  color: v-bind(dataAvailabilityColour)
}

</style>
