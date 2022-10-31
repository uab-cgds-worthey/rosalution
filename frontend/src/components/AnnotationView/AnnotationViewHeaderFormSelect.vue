<template>
  <select v-model="activeSelected" class="unit-select">
    <option v-for="genomcUnitOption in options" :key="genomcUnitOption">
      {{ genomcUnitOption }}
    </option>
  </select>
</template>

<script>
export default {
  name: 'annotation-view-header-form-select',
  emits: ['update:selected'],
  props: {
    selected: {
      type: String,
    },
    options: {
      type: Array,
    },
  },
  computed: {
    activeSelected: {
      get() {
        return this.selected;
      },
      set(value) {
        this.$emit('update:selected', value);
      },
    },
  },
};
</script>


<style scoped>

.unit-select {
  border: 1px solid transparent;
  border-radius: var(--content-border-radius);
  background-color: var(--primary-background-color);
  padding: var(--p-5);
  /* font-size: 1.5rem; 24px */
  font-size: 1.125rem; /* 18px */

  font-weight: 700;
  color: var(--rosalution-purple-300);
}

.unit-select:hover, .unit-select:focus, .unit-select:focus-within {
  border: 1px solid var(--rosalution-purple-300);
  box-shadow:  0px 0 0 4px rgba(69, 28, 137, 0.10);
  background-color: var(--secondary-background-color);
}

.unit-select:focus-visible {
  outline: var(--rosalution-purple-300) auto 2px;

}
</style>
