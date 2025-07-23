<template>
  <div class="section-row">
    <label class="section-field" v-bind:style="[fieldEmptyStyle]">
      {{ field }}
    </label>
    <span class="section-content">
      <MultilineEditableSpan v-if="editable"
        class="editable-section-content-values" 
        data-test="editable-value"
        v-model:content="content"
      />
      <span v-else v-for="(rowValue, index) in value" :key="index" data-test="value-row">
        {{ rowValue }}
      </span>
    </span>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import MultilineEditableSpan from '@/components/AnalysisView/MultilineEditableSpan.vue';
const props = defineProps({
  field: {
    type: String,
  },
  value: {
    type: Array,
    required: false,
    default: () => { return [] }
  },
  editable: {
    type: Boolean,
    default: false,
  },
});

const isEmptyField = props.value.length === 0 && !props.editable 
const fieldEmptyStyle =  isEmptyField ? 'color: var(--rosalution-grey-300);' : 'color: var(--rosalution-black);';
const content = ref(props.value)
watch(content, async(newContent) => {
  const contentRow = {
    field: props.field,
    value: newContent,
  };
  emits('update:sectionContent', contentRow);
});
</script>

<style scoped>
.section-row {
  display: flex;
  flex-direction: row;
  gap: var(--p-10);
  padding: var(--p-1);
}

.section-field {
  flex: 0 0 11.25rem;
  font-weight: 600;
}

.section-content {
  display: flex;
  flex-direction: column;
  flex: 1 0 0;
}

.editable-section-content-values {
  overflow: hidden;
  resize: both;
  border-top: none;
  border-right: none;
  border-left: none;
  border-bottom: 2px solid var(--rosalution-purple-200);
}

span:focus {
  color: var(--rosalution-purple-300);
  outline: none;
  box-shadow: 0px 5px 5px var(--rosalution-grey-200);
}
</style>
