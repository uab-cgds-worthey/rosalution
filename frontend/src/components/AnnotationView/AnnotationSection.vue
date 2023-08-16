<template>
  <div class="rosalution-section-container">
    <input type="checkbox" v-bind:id="section_toggle" />
    <div class="rosalution-section-header" :data-test="this.header">
      <h2 class="rosalution-section-header-text">
        {{header}}
      </h2>
      <span class="rosalution-section-center" data-test="header-datasets">
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
      <label class="collapsable-icon" v-bind:for="section_toggle">
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
    writePermissions: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      section_toggle: this.header.toLowerCase() + '_collapse',
    };
  },
  computed: {
    allowAttach() {
      if (this.genomicAttachmentType == '' || !this.writePermissions) {
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


input[type="checkbox"] {
  display: none;
}

.rosalution-section-container input[type="checkbox"]:checked ~ .section-row {
  display: none;
}

.rosalution-section-container input[type="checkbox"]:checked ~ img {
  display: none;
}

input[type="checkbox"]:checked ~ .rosalution-section-header > button ~ label.collapsable-icon {
  transform: scaleY(-1);
}
</style>


