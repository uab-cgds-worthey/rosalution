<template>
  <div class="discussion-reply">
    Discussion Reply here {{ content }}
  </div>
</template>

<script setup>
import {ref} from 'vue';

const props = defineProps({
  replyId: {
    type: String,
  },
  authorId: {
    type: String,
  },
  authorName: {
    type: String,
  },
  publishTimestamp: {
    type: String,
  },
  content: {
    type: String,
  },
  userClientId: {
    type: String,
  },
  actions: {
    type: Array,
  },
});

const emit = defineEmits(['reply:edit', 'reply:delete']);

const editReplyContent = this.content;
const editingReplyFlag = ref(false);

// functions

function editDiscussionReply() {
  console.log('Reply is being edited');
  editingReplyFlag.value = !editingReplyFlag.value;
}

function confirmEditReply() {
  console.log('Confirming Reply has been edited');
  this.$emit('reply:edit', this.id, editReplyContent);
}

function cancelEditReply() {
  console.log('Cancel Editing Reply');
}

function deleteDiscussionReply(replyId) {
  console.log('Confirm Reply has been Deleted');
  this.$emit('reply:delete', replyId);
}

</script>

<style scoped>

</style>
