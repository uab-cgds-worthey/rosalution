<template>
  <span role="textbox" contenteditable @input="onChange" class="editable-text">{{ editableContent }}</span>
</template>

<script setup>
const emits = defineEmits(['update:content']);
const props = defineProps({
  content: {
    type: Array,
    default: () => {
      return [];
    },
  },
});

const editableContent = props.content.join('\n');

function onChange(event) {
  emits('update:content', event.target.innerText.split('\n'));
}
</script>

<style>
.editable-text {
  display: inline-block;
  white-space: pre-wrap;
}
</style>
