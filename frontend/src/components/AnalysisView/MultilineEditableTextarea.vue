<template>
  <textarea contenteditable="plaintext-only" v-model="content"></textarea>
</template>

<script setup>
const content = defineModel('content', {
  get(value) {
    return value.join('\n');
  },
  set(value) {
    return value.split('\n');
  },
});
</script>
