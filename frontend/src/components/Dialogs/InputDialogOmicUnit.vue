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
      />
    </div>
    <div class="input-row">
      <span class="input-field">
        Reason of Interest
      </span>
      <textarea
        class="input-area"
        placeholder="Enter Reason of Interest."
        v-model="ROI"
      >
      </textarea>
    </div>
  </div>
</template>

<script setup>
import {ref, toRaw, computed} from 'vue';

defineOptions({
  name: 'input-dialog-omic-unit',
});

const props = defineProps({
  userInput: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(['update:userInput']);

const omicUnit = ref({
  refSeqTranscript: '',
  geneSymbol: '',
  cdna: '',
  protein: '',
  ROI: '',
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
