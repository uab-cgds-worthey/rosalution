<template>
  <div class="discussion-reply-container">
    <blockquote class="discussion-reply-quote">
      <div class="discussion-reply">
        <div class="discussion-reply-header">
          <div>
            <b>{{ authorName }}</b>
            {{  timestamp }}
          </div>
        </div>
        <div class="discussion-reply-content">
          {{content}}
        </div>
      </div>
    </blockquote>
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

.discussion-reply {
  border-radius: var(--content-border-radius);
  padding: var(--p-8);
  margin-top: var(--p-10);
  background-color: var(--rosalution-grey-50);
  margin-left: var(--p-8);
}

.discussion-reply-header {
  display: flex;
  justify-content: space-between;
  margin-top: var(--p-5);
  margin-bottom: var(--p-5);
}

.discussion-reply-content {
  margin-bottom: var(--p-10);
}

.discussion-reply-quote {
  border-left: var(--p-5) solid var(--rosalution-grey-50);
  /* padding-right: var(--p-8); */
}

</style>
