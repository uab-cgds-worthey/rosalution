<template>
  <textarea contenteditable="plaintext-only" v-model="content"></textarea>
</template>

<script setup>
const emits = defineEmits(['update:content']);

// const content = defineProps('content', {
//     type: Array,
//     default: () => { return [] },
// });

const content = defineModel('');

const editableContent = ref(props.content.join('\n'));

// function onChange(event) {
//   emits('update:content', event.target.innerText.split('\n'))
// }
</script>