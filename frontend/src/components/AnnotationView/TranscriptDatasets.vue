<template>
<div class="transcript-section">
  <div v-for="transcript in value" :key="transcript.transcript_id" class="transcript-item">
    <div class="transcript-header">
      <span class="transcript-header-text">
        {{transcript['transcript_id'] || 'RefSeq Transcript ID Unavailable'}}
      </span>
      <TextHighlightDataset
        label="Impact"
        :value="transcript['Impact']"
        :highlight="impactConfiguration"
      >
      </TextHighlightDataset>
    </div>
    <TextDataset label="Consequences" :value="transcript['Consequences']" style="grid-row:1;" :delimeter="`\n`" />
    <div class="section-content">
      <SetDataset
        label="SIFT"
        :value="transcript['SIFT Prediction']"
        :set="siftSetConfiguration"
      >
      </SetDataset>
      <SetDataset
        label="Polyphen"
        :value="transcript['Polyphen Prediction']"
        :set="polyphenSetConfiguration"
      >
      </SetDataset>
    </div>
  </div>
</div>
</template>

<script setup>
import SetDataset from '@/components/AnnotationView/SetDataset.vue';
import TextDataset from '@/components/AnnotationView/TextDataset.vue';
import TextHighlightDataset from '@/components/AnnotationView/TextHighlightDataset.vue';

defineProps({
  value: {
    type: [Array],
  },
});

const impactConfiguration = {
  'MODERATE': 'Yellow',
  'MODIFIER': 'Green',
  'HIGH': 'Red',
};
const polyphenSetConfiguration = [
  {value: 'probably_damaging', classification: 'Probably Damaging', colour: 'Red'},
  {value: 'possibly_damaging', classification: 'Possibly Damaging', colour: 'Yellow'},
  {value: 'benign', classification: 'Benign', colour: 'Blue'},
];

const siftSetConfiguration = [
  {value: 'deleterious_low_confidence', classification: 'Deleterious Low Confidence', colour: 'Red'},
  {value: 'deleterious', classification: 'Deleterious', colour: 'Red'},
  {value: 'tolerated', classification: 'Tolerated', colour: 'Blue'},
];
</script>
