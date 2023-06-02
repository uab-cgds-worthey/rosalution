<template>
  <div class="rosalution-section-container">
    <div style="background-color: red;">
      <input v-if="!this.edit" type="checkbox" v-bind:id="section_toggle" />
      <div class="rosalution-section-header">
        <h2 class="rosalution-section-header-text">
          {{ header }}
        </h2>
        <span class="rosalution-section-center"></span>
        <span class="rosalution-header-right-icons">
          <label v-if="this.attachmentField" class="attach-logo" @click="$emit('attach-image', this.header, this.attachmentField)">
            <font-awesome-layers class="fa-md">
              <font-awesome-icon :icon="['fa', 'file-circle-plus']" />
              <font-awesome-icon transform="shrink-9.5 left-4.5 down-3" inverse :icon="['fa', 'mountain-sun']"/>
            </font-awesome-layers>
          </label>
          <label v-if="this.edit" class="edit-logo" id="edit-logo">
            <font-awesome-icon icon="pencil" size="lg" />
          </label>
          <label v-else class="collapsable-logo" v-bind:for="section_toggle">
            <font-awesome-icon icon="chevron-down" size="lg" />
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
        :value="contentRow.value"
        :data-test="contentRow.field"
        @update:section-text="this.onContentChanged"
      />
    </div>
  </div>
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
  created() {
    console.log(this.contentList);
    console.log('on created');
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
  },
};
</script>

<style scoped>
.attach-logo {
  color: var(--rosalution-purple-300);
  cursor: pointer;
}

.collapsable-logo {
  color: var(--rosalution-grey-200);
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

.rosalution-section-container input[type="checkbox"]:checked~.field-value-row {
  display: none;
}

.rosalution-section-container input[type="checkbox"]:checked~img {
  display: none;
}

input[type="checkbox"]:checked~tr>td>label.collapsable-logo {
  transform: scaleY(-1);
}
</style>
