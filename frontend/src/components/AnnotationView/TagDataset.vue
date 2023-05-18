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
.dataset-container {
  display: flex;
  padding: var(--p-1);
  line-height: 1.5rem;
}

.dataset-label {
  flex: 0 0 130px;
  font-weight: 600;
  color: v-bind(dataAvailabilityColour)
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: var(--p-8) var(--p-1);
}

.tag {
  padding: var(--p-1) var(--p-8);
  background-color: transparent;
  border-radius: var(--p-16);
  border: 2px solid var(--rosalution-black);
  color: var(--rosalution-black);
}

a:hover {
  color: var(--rosalution-purple-100);
}

.text-value {
  white-space: pre-wrap;
}
</style>
