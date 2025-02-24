<template>
  <div class="dataset-container">
    <DatasetLabel :label="label" :datasetValue="value"></DatasetLabel>
    <div class="dataset-bar" v-bind="datasetBarAttributes" data-test="score-background">
      <div v-if="isAvailable" class="score-fill"
        :style="{
                'background-color': scoreStyling.fillColour,
                width: scoreFillWidthPercentage,
              }" data-test="score-fill">
      </div>
    </div>
    <span class="score-text" :style="{ color: scoreStyling.textColour }" data-test="score-text">
        {{ value }}
      </span>
  </div>
</template>

<script setup>

import DatasetLabel from '@/components/AnnotationView/DatasetLabel.vue';

import {isDatasetAvailable, useScoreBarCalculations} from '@/components/AnnotationView/datasetRenderingUtility.js';

const props = defineProps({
  label: {
    type: String,
  },
  value: {
    type: [Number, String],
  },
  minimum: {
    type: Number,
  },
  maximum: {
    type: Number,
  },
  bounds: {
    type: Object,
  },
  cutoff: {
    type: Number,
  },
});

const styles = {
  unavailableColours: {
    fillColour: '',
    backgroundColour: 'var(--rosalution-grey-100)',
    borderColour: '',
    textColour: 'var(--rosalution-grey-300)',
  },
  nominalColours: {
    fillColour: 'var(--rosalution-blue-200)',
    backgroundColour: 'var(--rosalution-blue-300)',
    borderColour: 'var(--rosalution-blue-100)',
    textColour: 'var(--rosalution-blue-300)',
  },
  closeToThresholdColours: {
    fillColour: 'var(--rosalution-yellow-200)',
    backgroundColour: 'var(--rosalution-yellow-300)',
    borderColour: 'var(--rosalution-yellow-100)',
    textColour: 'var(--rosalution-yellow-300)',
  },
  outOfThresholdColours: {
    fillColour: 'var(--rosalution-red-200)',
    backgroundColour: 'var(--rosalution-red-300)',
    borderColour: 'var(--rosalution-red-100)',
    textColour: 'var(--rosalution-red-300)',
  },
};

const isAvailable = isDatasetAvailable(props.value);
const {scoreFillWidthPercentage, datasetBarAttributes, scoreStyling} =
  useScoreBarCalculations(props.value, props, styles);

</script>
