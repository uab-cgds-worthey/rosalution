<template>
    <font-awesome-icon :icon="['far', 'copy']" class="copy-icon" @click="copyToClipboard()"/>
</template>

<script setup>
const props = defineProps({
  copyText: {
    type: String,
    required: true,
  },
});

const emits = defineEmits(['clipboard-copy']);

async function copyToClipboard() {
  /* Needed to add a try/catch to can an error that occurs in Cypress, which causes the test to fail. */
  try {
    await navigator.clipboard.writeText(props.copyText);
  } catch (error) {
    console.error(error.message);
  }

  emits('clipboard-copy', props.copyText);
}
</script>

<style>
.copy-icon:hover {
  cursor: pointer;
}

.copy-icon:active {
  color: var(--rosalution-purple-200)
}</style>
