<template>
  <div class="rosalution-section-container">
    <div class="rosalution-section-header">
      <span>
        <h2 class="rosalution-section-header-text">
          {{header}}
        </h2>
      </span>
      <span class="rosalution-section-center">
        <slot name="headerDatasets"></slot>
      </span>
      <button
        v-if="allowAttach"
        class="attach-logo"
        @click="$emit('attach-image', attachmentDataset, genomicAttachmentType)"
        data-test="attach-logo"
      >
      <font-awesome-icon :icon="['fa', 'paperclip']" size="xl" />
      </button>
      <label class="collapsable-icon">
        <font-awesome-icon icon="chevron-down" size="lg"/>
      </label>
    </div>
    <div class="rosalution-section-seperator"></div>
    <slot></slot>
  </div>
</template>

<script>

export default {
  name: 'annotation-section',
  props: {
    header: {
      type: String,
    },
    attachmentDataset: {
      type: String,
      default: '',
    },
    genomicAttachmentType: {
      type: String,
      default: '',
    },
  },
  computed: {
    allowAttach() {
      if (this.genomicAttachmentType == '') {
        return false;
      }

      return true;
    },
  },
};
</script>

<style scoped>

.collapsable-icon {
  color: var(--rosalution-grey-200);
  cursor: pointer;
}

.attach-logo {
  color: var(--rosalution-purple-300);
  background: none;
  border: none;
  float: right;
  cursor: pointer;
}

</style>
