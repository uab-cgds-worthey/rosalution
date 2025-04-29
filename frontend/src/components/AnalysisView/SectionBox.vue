<template>
  <div class="rosalution-section-container">
    <div>
      <input v-if="!this.edit" type="checkbox" v-bind:id="section_toggle" />
      <div class="rosalution-section-header">
        <h2 class="rosalution-section-header-text">
          {{ header }}
        </h2>
        <span class="rosalution-section-center"></span>
        <span class="rosalution-header-right-icons">
          <label v-if="this.allowAttach" class="attach-logo"
            @click="$emit('attach-image', this.header, this.attachmentField)"
            :data-test="`attach-logo-${header}`"
          >
            <font-awesome-layers class="fa-md">
              <font-awesome-icon :icon="['fa', 'file-circle-plus']" />
              <font-awesome-icon
                transform="shrink-9.5 left-4.5 down-3"
                inverse
                :icon="['fa', 'mountain-sun']"
              />
            </font-awesome-layers>
          </label>
          <label v-if="this.edit" class="edit-logo" id="edit-logo">
            <font-awesome-icon icon="pencil" size="lg" />
          </label>
          <label v-else class="collapsable-icon" v-bind:for="section_toggle">
            <font-awesome-icon icon="chevron-down" size="lg" :data-test="`collapsable-icon-${header}`" />
          </label>
        </span>
      </div>
      <div class="rosalution-section-seperator"></div>
      <component
        v-for="(contentRow, index) in this.contentList"
        :key="`${contentRow.field}-${index}`"
        :is="contentRow.type"
        :editable="this.edit"
        :field="contentRow.field"
        :dataSet="contentRow.field"
        :value="contentRow.value"
        :writePermissions="this.writePermissions"
        :data-test="contentRow.field"
        @update-annotation-image="this.onUpdateImageEmit"
        @update:section-content="this.onContentChanged"
        @download="this.onDownload"
      />
    </div>
  </div>
</template>

<script>
import ImagesDataset from '@/components/AnnotationView/ImagesDataset.vue';
import SectionText from '@/components/AnalysisView/SectionText.vue';
import SectionAttachment from '@/components/AnalysisView/SectionAttachment.vue';

export default {
  name: 'section-box',
  emits: ['update:contentRow', 'attach-image', 'update-image', 'download'],
  components: {
    SectionText,
    ImagesDataset,
    SectionAttachment,
  },
  props: {
    analysis_name: {
      type: String,
    },
    header: {
      type: String,
    },
    attachmentField: {
      type: String,
      default: '',
    },
    writePermissions: {
      type: Boolean,
      default: true,
    },
    content: {
      type: Array,
    },
    edit: {
      type: Boolean,
    },
  },
  data() {
    return {
      contentList: this.content,
      section_toggle: this.header.toLowerCase() + '_collapse',
    };
  },
  computed: {
    allowAttach() {
      if (this.attachmentField == '' || !this.writePermissions) {
        return false;
      }

      return true;
    },
    hasAttachmentContent() {
      return this.attachmentField.length > 0;
    },
    sectionImageExist() {
      for (const rowContent of this.contentList) {
        if (rowContent.dataset && rowContent.dataset === this.attachmentField) {
          return rowContent.value > 0;
        }
      }

      return false;
    },
  },
  methods: {
    onContentChanged(sectionContent) {
      const contentRow = {
        header: this.header,
        ...sectionContent,
      };
      this.$emit('update:contentRow', contentRow);
    },
    onUpdateImageEmit(imageId, field) {
      this.$emit('update-image', imageId, this.header, field);
    },
    onDownload(content) {
      this.$emit('download', content);
    },
  },
};
</script>

<style scoped>
.attach-logo {
  color: var(--rosalution-purple-300);
  cursor: pointer;
}

.edit-logo {
  color: var(--rosalution-purple-100);
}

span:focus {
  color: var(--rosalution-purple-300);
  outline: none;
  box-shadow: 0px 5px 5px var(--rosalution-grey-200);
}

input[type="checkbox"] {
  display: none;
}

</style>
