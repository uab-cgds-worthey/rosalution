<template>
  <div class="discussion-reply-container">
    <div class="discussion-reply">
      <div class="discussion-reply-header">
        <b>{{ authorName }}</b>
          {{  timestamp }}
      </div>
      {{content}}
    </div>
  </div>
</template>

<script setup>
import {computed, ref} from 'vue';

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

const editReplyContent = props.content;
const editingReplyFlag = ref(false);

// computed

const timestamp = computed(() => {
  return new Date(props.publishTimestamp + 'Z').toLocaleString();
});

// functions



function editDiscussionReply() {
  console.log('Reply is being edited');
  editingReplyFlag.value = !editingReplyFlag.value;
}

function confirmEditReply() {
  console.log('Confirming Reply has been edited');
  emit('reply:edit', props.id, editReplyContent);
}

function cancelEditReply() {
  console.log('Cancel Editing Reply');
}

function deleteDiscussionReply(replyId) {
  console.log('Confirm Reply has been Deleted');
  emit('reply:delete', replyId);
}

</script>

<style scoped>

</style>
