<template>
  <div class="dataset-container">
    <DatasetLabel :label="label" :datasetValue="value"></DatasetLabel>
    <span class="set-section">
      <span v-if="!value || availableData"
        class="set-background set-fill-unavailable set-fill"
        data-test="set-unavailable">
      </span>
        <span v-else class="set-background set-text set-fill" data-test="set-fill">
          <span v-for="(item, index) in set"
            :key="`${value}-${index}`"
            :style="setItemStyle(item)"
          >
            {{ classificationText(item) }}
          </span>
        </span>
      </span>
  </div>
</template>

<script setup>
import DatasetLabel from '@/components/AnnotationView/DatasetLabel.vue';

import {isDatasetAvailable} from '@/components/AnnotationView/datasetRenderingUtility.js'

const props = defineProps({
  label: {
    type: String,
  },
  value: {
    type: String,
  },
  set: {
    type: Array,
    default: () => {
      return [];
    },
  },
  ticker: {
    type: Boolean,
    default: false,
  },
})

const availableData = isDatasetAvailable(props.value);

function calculateWidth(value) {
  const width = 100;

  if (value == props.value) {
    return `${width * .75}%`;
  }
  return `${ (width / props.set.length) / 2}%`;
};

function setItemStyle(item) {
  const style = {
    'background-color': 'var(--rosalution-grey-300)',
    'opacity': 1,
  };


  if (item.colour == 'Red') {
    style['background-color'] = 'var(--rosalution-red-200)';
  } else if (item.colour == 'Blue') {
    style['background-color'] = 'var(--rosalution-blue-200)';
  } else if (item.colour == 'Yellow') {
    style['background-color'] = 'var(--rosalution-yellow-200)';
  } else if (item.colour == 'Green') {
    style['background-color'] = 'var(--rosalution-green-200)';
  }

  style['width'] = calculateWidth(item.value);

  return (item.value == this.value) ? style : {...style, 'opacity': 0.5};
};

function classificationText(setItem) {
  return (setItem.value == props.value) ? setItem.classification : '';
};
</script>
