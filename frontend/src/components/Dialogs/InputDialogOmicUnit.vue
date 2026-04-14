<template>
  <div>
    <div class="input-row">
      <span class="input-field">
        RefSeq Transcript
      </span>
      <input
        class="input-area"
        placeholder="Enter Transcript"
        v-model="refSeqTranscript"
        data-test="refseq-transcript-input"
        :readonly="isEditing"
      />
    </div>
    <div class="input-row">
      <span class="input-field">
        Gene Symbol
      </span>
      <input
        class="input-area"
        placeholder="Enter Gene Symbol"
        v-model="geneSymbol"
        data-test="gene-symbol-input"
        :readonly="isEditing"
      />
    </div>
    <div class="input-row">
      <span class="input-field">
        cDNA
      </span>
      <input
        class="input-area"
        placeholder="Enter cDNA"
        v-model="cdna"
        data-test="hgvs-cdna-input"
        :readonly="isEditing"
      />
    </div>
    <div class="input-row">
      <span class="input-field">
        Protein
      </span>
      <input
        class="input-area"
        placeholder="Enter Protein"
        v-model="protein"
        data-test="hgvs-protein-input"
        :readonly="isEditing"
      />
    </div>
    <div class="input-row">
      <span class="input-field">
        Reason of Interest
      </span>
      <MultilineEditableTextarea
        class="input-area"
        placeholder="Enter Reason of Interest."
        v-model:content="ROI"
        data-test="reason-of-interest-input"
      />
    </div>
  </div>
</template>

<script setup>
import {ref, toRaw, computed} from 'vue';

import MultilineEditableTextarea from '@/components/AnalysisView/MultilineEditableTextarea.vue';

defineOptions({
  name: 'input-dialog-omic-unit',
});

const props = defineProps({
  userInput: {
    type: Object,
    required: true,
  },
});

const isEditing = props.userInput.edit !== undefined;

console.log(props.userInput)
const emit = defineEmits(['update:userInput']);

const omicUnit = ref({
  refSeqTranscript: props.userInput.data['refSeqTranscript'],
  geneSymbol:  props.userInput.data['geneSymbol'],
  cdna: props.userInput.data['cdna'],
  protein: props.userInput.data['protein'],
  ROI: props.userInput.data['ROI'],
});

const refSeqTranscript = computed({
  get() {
    return omicUnit.value['refSeqTranscript'];
  },
  set(value) {
    omicUnit.value['refSeqTranscript'] = value;
    omicUnitUpdated();
  },
});

const geneSymbol = computed({
  get() {
    return omicUnit.value['geneSymbol'];
  },
  set(value) {
    omicUnit.value['geneSymbol'] = value;
    omicUnitUpdated();
  },
});

const cdna = computed({
  get() {
    return omicUnit.value['cdna'];
  },
  set(value) {
    omicUnit.value['cdna'] = value;
    omicUnitUpdated();
  },
});

const protein = computed({
  get() {
    return omicUnit.value['protein'];
  },
  set(value) {
    omicUnit.value['protein'] = value;
    omicUnitUpdated();
  },
});

const ROI = computed({
  get() {
    return omicUnit.value['ROI'];
  },
  set(value) {
    omicUnit.value['ROI'] = value;
    omicUnitUpdated();
  },
});

const editingOmicUnit = computed({

});

function omicUnitUpdated() {
  const input = props.userInput;
  input['data'] = omicUnit.value;
  emit('update:userInput', toRaw(input));
}


</script>

<style scoped>

.input-row {
  display: flex;
  padding: var(--p-10);
  gap: var(--p-24);
  justify-content: space-between;
}

.input-field {
  font-weight: bold;
}

.input-area {
  max-width: fit-content;
  min-width: 250px;
}

</style>
