<template>
  <div>
  <hr>
  <div class="dataset-container">
    <div v-for="transcript in value" :key="transcript.transcript_id" class="transcript-container">
      <div class="transcript-header">
        <h2 class="transcript-header-text"> {{transcript['transcript_id'] || 'RefSeq Transcript ID Unavailable'}} </h2>
        <TextHighlightDataset
          label="Impact"
          :value="transcript['Impact']"
          :highlight="this.impactConfiguration"
        >
        </TextHighlightDataset>
      </div>
      <div><TextDataset label="Consequences" :value="transcript['Consequences']" :delimeter="`\n`"></TextDataset></div>
      <div class="transcript-scores">
        <SetDataset
          label="SIFT"
          :value="transcript['SIFT Prediction']"
          :set="this.siftSetConfiguration"
        >
        </SetDataset>
        <SetDataset
          label="Polyphen"
          :value="transcript['Polyphen Prediction']"
          :set="this.polyphenSetConfiguration"
        >
        </SetDataset>
        <div class="blank-transcript-score-spot"></div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import SetDataset from '@/components/AnnotationView/SetDataset.vue';
import TextDataset from '@/components/AnnotationView/TextDataset.vue';
import TextHighlightDataset from '@/components/AnnotationView/TextHighlightDataset.vue';

export default {
  name: 'transcript-datasets',
  components: {
    TextDataset,
    SetDataset,
    TextHighlightDataset,
  },
  props: {
    value: {
      type: [Array],
    },
  },
  data: function() {
    return {
      impactConfiguration: {
        'MODERATE': 'Yellow',
        'MODIFIER': 'Green',
        'HIGH': 'Red',
      },
      polyphenSetConfiguration: [
        {value: 'probably_damaging', classification: 'Probably Damaging', colour: 'Red'},
        {value: 'possibly_damaging', classification: 'Possibly Damaging', colour: 'Yellow'},
        {value: 'benign', classification: 'Benign', colour: 'Blue'},
      ],
      siftSetConfiguration: [
        {value: 'deleterious_low_confidence', classification: 'Deleterious Low Confidence', colour: 'Red'},
        {value: 'deleterious', classification: 'Deleterious', colour: 'Red'},
        {value: 'tolerated', classification: 'Tolerated', colour: 'Blue'},
      ],
    };
  },
  computed: {
    isDataUnavailable: function() {
      return this.value == '.' || this.value == 'null' || this.value == null;
    },
    dataAvailabilityColour: function() {
      return this.isDataUnavailable ?
            'var(--rosalution-grey-300)' :
            this.linkout ? 'var(--rosalution-purple-300)' :
                'var(--rosalution-black)';
    },
  },
};
</script>
