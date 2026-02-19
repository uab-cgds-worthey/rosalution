<template>
  <div>
    <div class="dialog-header"
      @click="logAnalysisName"
    >
      Please enter unit of interest for this case. {{ props.analysis }}
    </div>
    <div class="input-row">
      <span class="input-field">
        RefSeq Transcript
      </span>
      <input
        class="input-area"
        placeholder="Enter Transcript"
      />
    </div>
    <div class="input-row">
      <span class="input-field">
        Gene Symbol
      </span>
      <input
        class="input-area"
        placeholder="Enter Gene Symbol"
      />
    </div>
    <div class="input-row">
      <span class="input-field">
        cDNA
      </span>
      <input
        class="input-area"
        placeholder="Enter cDNA"
      />
    </div>
    <div class="input-row">
      <span class="input-field">
        Protein
      </span>
      <input
        class="input-area"
        placeholder="Enter Protein"
      />
    </div>
    <div class="input-row">
      <span class="input-field">
        Reason of Interest
      </span>
      <textarea
        class="input-area"
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
  analysis: {
    type: String,
    default: () => {
      return '';
    },
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

function logAnalysisName() {
  console.log(props.analysisName);
}

</script>

<style scoped>

.dialog-header {
  padding: var(--p-8);
  text-align: center;
}

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
