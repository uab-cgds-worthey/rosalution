<template>
  <table class="rosalution-section-container">
    <tbody>
      <tr class="rosalution-section-header">
        <td>
          <h2 class="rosalution-section-text">
            {{header}}
          </h2>
        </td>
        <td class="rosalution-section-center">
          <slot name="headerDatasets"></slot>
        </td>
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
      </tr>
      <div class="rosalution-section-seperator"></div>
      <slot></slot>
    </tbody>
  </table>
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
table {
  width:100%;
}

.section-name {
  margin: var(--p-1) var(--p-1) 0 var(--p-1);
}

.section-center {
  flex-grow: 2;
  /* justify-content: flex-start; */
}

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

.seperator {
  height: .125rem;
  background-color: var(--rosalution-grey-100);
  border: solid .0469rem var(--rosalution-grey-100);
}

</style>
