<template>
  <div>
    <div class="dialog-header">
      Please enter unit of interest for this case. {{ props.analysisName }}
    </div>
    <div class="input-row">
      <span class="transcript-input-field">
        RefSeq Transcript
      </span>
      <input
        class="transcript-input"
        placeholder="Enter Transcript"
      />
    </div>
    <div class="input-row">
      <span class="gene-input-field">
        Gene Symbol
      </span>
      <input
        class="gene-input"
        placeholder="Enter Gene Symbol"
      />
    </div>
    <div class="input-row">
      <span class="cDNA-input-field">
        cDNA
      </span>
      <input
        class="cDNA-input"
        placeholder="Enter cDNA"
      />
    </div>
    <div class="input-row">
      <span class="protein-input-field">
        Protein
      </span>
      <input
        class="protein-input"
        placeholder="Enter Protein"
      />
    </div>
    <div class="input-row">
      <span class="reason-of-interest-input-field">
        Reason of Interest
      </span>
      <textarea
        class="reason-of-interest-input"
        placeholder="Enter Reason of Interest."
      >
      </textarea>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref, toRaw} from 'vue';

const omicUnit = ref({});

defineOptions({
  name: 'input-dialog-omic-unit',
});

const props = defineProps({
  userInput: {
    type: Object,
    required: false,
  },
  analysisName: {
    type: String,
  },
  omicUnit: {
    type: Object,
    default: () => {
      return {};
    },
  },
});

onMounted(async () => {
});

</script>

<style scoped>

.input-row {
  display: flex;
  padding: var(--p-8);
  gap: var(--p-10);
  justify-content: space-between;
}

.gene-input {
  /* padding: var(--p-8); */
  /* margin: var(--p-8); */
}

</style>
