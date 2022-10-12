<template>
  <div class="dataset-container">
    <a :href="linkout" class="dataset-label" data-test="text-label"
       target="_blank" ref="noreferrer noopener">
      {{ label }}
      <font-awesome-icon icon="up-right-from-square" size="2xs"/>
    </a>
  </div>
</template>

<script>
export default {
  name: 'clinvar-dataset',
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
  },
};
</script>

<style scoped>

.dataset-container {
  display: flex;
  padding: var(--p-1);
  padding-top: var(--p-10);
  line-height: 24px; /**temproary until I see how things look */
}

.dataset-label {
  flex: 0 0 125px;
  font-weight: 600;
  color: var(--rosalution-purple-300);
  font-size: 1.25rem;
};

a:hover .dataset-label {
  color: var(--rosalution-purple-100);
}

</style>
