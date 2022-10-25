<template>
  <div class="dataset-container">
    <a :href="linkout"
      class="dataset-label"
      :class="isLinkoutAvailable ? 'dataset-label-available' : 'dataset-label-unavailable'"
      data-test="text-label"
      target="_blank" ref="noreferrer noopener"
    >
      {{ label }}
      <font-awesome-icon v-if="isLinkoutAvailable" icon="up-right-from-square" size="2xs"/>
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
      default: () => {
        return [];
      },
    },
  },
  computed: {
    isDataAvailable: function() {
      return !(this.value == '.' || this.value == 'null' || this.value == null || typeof(this.value) != 'undefined');
    },
    isLinkoutAvailable() {
      return typeof(this.linkout) !== 'undefined';
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
  font-size: 1.25rem;
};

.dataset-label-available {
  color: var(--rosalution-purple-300)
}

.dataset-label-unavailable {
  color: var(--rosalution-grey-100)
}

a:hover .dataset-label {
  color: var(--rosalution-purple-100);
}

</style>
