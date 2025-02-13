<template>
    <div class="dataset-container">
      <DatasetLabel :label="label" :linkout="linkout" :datasetValue="value"></DatasetLabel>
      <div class="tags-container">
        <div class="tag" v-for="(item, index) in content" :key="index">
        {{ item }}
      </div>
      </div>
    </div>
</template>

<script setup>
import DatasetLabel from '@/components/AnnotationView/DatasetLabel.vue';

const props = defineProps({
  label: {
    type: String,
    required: false,
  },
  linkout: {
    type: String,
    required: false,
  },
  value: {
    type: [String, Array],
    default: '',
  },
  delimeter: {
    type: String,
    default: ';   ',
  },
});

const content = (typeof(props.value) == 'object') ?  props.value : props.value.split(props.delimeter);
</script>


