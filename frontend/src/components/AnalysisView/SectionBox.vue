<template>
  <table class="rosalution-section-container">
    <tbody>
      <input v-if="!this.edit" type="checkbox" v-bind:id="section_toggle" />
      <tr class="rosalution-section-header">
        <td>
          <h2 class="rosalution-section-text">
            {{ header }}
          </h2>
        </td>
        <td class="rosalution-section-center"></td>
        <button v-if="this.attachmentField" class="attach-logo" @click="$emit(this.sectionImageOperation(), this.header, this.attachmentField)">
          <font-awesome-icon :icon="['fa', 'paperclip']" size="xl" />
        </button>
        <label v-if="this.edit" class="edit-logo" id="edit-logo">
          <font-awesome-icon icon="pencil" size="lg" />
        </label>
        <label v-else class="collapsable-logo" v-bind:for="section_toggle">
          <font-awesome-icon icon="chevron-down" size="lg" />
        </label>
      </tr>
      <div class="rosalution-section-seperator"></div>
      <component
        v-for="(contentRow, index) in this.contentList"
        :key="`${contentRow.field}-${index}`"
        :is="contentRow.type"
        :editable="this.edit"
        :field="contentRow.field"
        :value="contentRow.value"
        :data-test="contentRow.field"
        @update:section-text="this.onContentChanged"
      />
    </tbody>
  </table>
</template>

<script>
import ImagesDataset from '@/components/AnnotationView/ImagesDataset.vue';
import SectionText from '@/components/AnalysisView/SectionText.vue';


export default {
  name: 'section-box',
  components: {
    SectionText,
    ImagesDataset,
  },
  emits: ['update:contentRow', 'attach-image', 'update-image'],
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
    hasAttachmentContent() {
      return (this.attachmentField.length > 0);
    },
    sectionImageExist() {
      console.log('section image existing?')
      for ( const rowContent of this.contentList ) {
        if (rowContent.dataset && rowContent.dataset === this.attachmentField) {
          return rowContent.value > 0;
        }
      }

      return false;
    },
  },
  methods: {
    onContentChanged(sectionText) {
      const contentRow = {
        header: this.header,
        ...sectionText,
      };
      console.log(contentRow);
      console.log('content row');
      this.$emit('update:contentRow', contentRow);
    },
    sectionImageOperation() {
      console.log('section image operation select?')
      // if (this.sectionImageExist) {
      //   return 'update-image';
      // }
      return 'attach-image';
    },
  },
};
</script>

<style scoped>
table {
  width: 100%;
}

div {
  font-family: "Proxima Nova", sans-serif;
  padding: var(--p-0);
}

.section-name {
  /* height: 1.75rem; */
  margin: .125rem .125rem 0 .125rem;
  /* flex: 1 0 auto; */
}

.attach-logo {
  color: var(--rosalution-purple-300);
  background: none;
  border: none;
  cursor: pointer;
}

.collapsable-logo {
  color: var(--rosalution-grey-200);
  cursor: pointer;
}

.section-row {
  display: flex;
  flex-direction: row;
  gap: var(--p-10);
  margin: var(--p-10) var(--p-1) var(--p-10) var(--p-1);
}

.section-field {
  display: inline-block;
  width: 11.25rem;
  height: 1.375rem;
  margin: 0 1.1875rem .0063rem 0;
  font-size: 1.125rem;
  font-weight: 600;
  text-align: left;
}

.section-content {
  font-size: 1.125rem;
  text-align: left;
  color: var(--rosalution-black);
  display: block;
}

.section-content-values {
  font-size: 1.125rem;
  color: var(--rosalution-black);
  display: block;
  width: 100%;
}

.edit-logo {
  color: var(--rosalution-purple-100);
}

.editable-section-content-values {
  display: block;
  width: 100%;
  overflow: hidden;
  resize: both;
  border-top: none;
  border-right: none;
  border-left: none;
  border-bottom: 2px solid var(--rosalution-purple-200);
  font-family: inherit;
  font-size: inherit;
}

span:focus {
  color: var(--rosalution-purple-300);
  outline: none;
  box-shadow: 0px 5px 5px var(--rosalution-grey-200);
}

input[type="checkbox"] {
  display: none;
}

.section-box-container input[type="checkbox"]:checked~.field-value-row {
  display: none;
}

.section-box-container input[type="checkbox"]:checked~img {
  display: none;
}

input[type="checkbox"]:checked~tr>td>.collapsable-logo {
  transform: scaleY(-1);
}
</style>
