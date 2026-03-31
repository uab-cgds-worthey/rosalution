<template>
  <div class="dataset-container">
    <DatasetLabel :label="label" :linkout="linkout" :datasetValue="value"></DatasetLabel>
    <span class="text-value" data-test="text-value" >{{ content }}</span>
    <CopyToClipboard
      v-if="props.enableCopy && content"
      :copyText="content"
      @clipboard-copy="emits('clipboard-copy', content)"
    ></CopyToClipboard>
  </div>
</template>

<script setup>
import {ref} from 'vue';
import DatasetLabel from '@/components/AnnotationView/DatasetLabel.vue';
import CopyToClipboard from '@/components/CopyToClipboard.vue';

const emits = defineEmits(['clipboard-copy']);

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
  enableCopy: {
    type: Boolean,
    default: false,
  },
});

function calculateContent() {
  if (props.value == null || props.value == undefined) {
    return '';
  }

  return ( typeof(props.value) == 'object')?props.value.join(props.delimeter) : props.value;
}

const content = ref(calculateContent());
</script>
