<template>
  <div class="dataset-container">
    <DatasetLabel :label="label" :linkout="linkout" :datasetValue="value"></DatasetLabel>
    <span class="text-value" data-test="text-value" >{{ content }}</span>
  </div>
</template>

<script setup>
import {ref} from 'vue'
import DatasetLabel from '@/components/AnnotationView/DatasetLabel.vue';

const props = defineProps({
  label: {
    type: String,
    required: false
  },
  linkout: {
    type: String,
    required: false,
  },
  value: {
    type: [String, Array],
    default: "",
  },
  delimeter: {
    type: String,
    default: ';   ',
  },
});

function calculateContent() {
  if(props.value == null || props.value == undefined) {

    console.log(`Dataset ${props.label} not defined`)
    return ""
  }

  return ( typeof(props.value) == 'object')?props.value.join(props.delimeter) : props.value
}

const content = ref(calculateContent())

</script>
