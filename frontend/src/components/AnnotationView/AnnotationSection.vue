<template>
  <div class="rosalution-section-container annotation-section-container">
    <input type="checkbox" v-bind:id="section_toggle" />
    <div class="rosalution-section-header annotation-section-header" :data-test="this.header">
      <h2 class="annotation-section-header-text">
        {{header}}
      </h2>
      <span class="rosalution-section-center" data-test="header-datasets">
        <slot name="headerDatasets"></slot>
      </span>
      <label
        v-if="allowAttach"
        class="attach-logo"
        @click="$emit('attach-image', attachmentDataset, genomicAttachmentType)"
        data-test="attach-logo"
      >
        <font-awesome-layers font-awesome-layers class="fa-md">
          <font-awesome-icon :icon="['fa', 'file-circle-plus']" />
          <font-awesome-icon
            transform="shrink-9.5 left-4.5 down-3"
            inverse
            :icon="['fa', 'mountain-sun']"
          />
        </font-awesome-layers>
      </label>
      <label class="collapsable-icon" v-bind:for="section_toggle">
        <font-awesome-icon icon="chevron-down" size="lg"/>
      </label>
    </div>
    <div class="rosalution-section-seperator annotation-section-seperator"></div>
    <div class="section-content">
      <slot></slot>
  </div>
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
  margin-right: var(--p-8);
}


input[type="checkbox"] {
  display: none;
}

.rosalution-section-container input[type="checkbox"]:checked ~ .section-content {
  display: none;
}

input[type="checkbox"]:checked ~ .rosalution-section-header > span ~ label.collapsable-icon {
  transform: scaleY(-1);
}
</style>


