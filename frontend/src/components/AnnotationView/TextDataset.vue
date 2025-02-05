<template class="dataset-container">
  <div class="dataset-container">
    <DatasetLabel></DatasetLabel>
    <span class="text-value" data-test="text-value" >{{ content }}</span>
  </div>
</template>

<script>
import DatasetLabel from '@/components/AnnotationView/DatasetLabel.vue';

const props = defineProps({
  label: {
    type: String,
  },
  linkout: {
    type: String,
    required: false,
  },
  value: {
    type: [String, Array],
  },
  delimeter: {
    type: String,
    default: ';   ',
  },
});

const content =  (typeof(props.value) == 'object') ? props.value.join(props.delimeter) : props.value;

</script>
