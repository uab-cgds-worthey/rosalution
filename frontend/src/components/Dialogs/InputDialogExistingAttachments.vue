<template>
  <div class="attach-supporting-evidence">
  </div>
</template>

<script>
export default {
  name: 'input-dialog-existing-attachments',
  emits: ['update:userInput'],
  props: {
    userInput: {
      type: Object,
      required: true,
    },
    existingAttachments: {
      type: Array,
      default: () => {
        return [];
      },
    },
  },
  computed: {
  },
  methods: {
  },
};
</script>

<style scoped>

</style>
