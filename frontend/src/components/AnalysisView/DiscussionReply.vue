<template>
  <div class="discussion-reply-container">
    <blockquote class="discussion-reply-quote">
      <div class="discussion-reply">
        <div class="discussion-reply-header">
          <div>
            <b>{{ authorName }}</b>
            {{  timestamp }}
          </div>
          <ul v-if="isUser" class="context-menu" data-test="discussion-reply-context-menu">
            <ContextMenu
              :actions="actions"
              :contextId="replyId"
              @edit="editDiscussionReply"
              @delete="deleteDiscussionReply"
              >
              <font-awesome-icon class="header-icon" icon="ellipsis-vertical" size="xl" />
            </ContextMenu>
          </ul>
        </div>
        <div v-if="!editingReplyFlag.value" class="discussion-reply-content">
          {{content}}
        </div>
        <div v-else class="discussion-edit-reply">
          <textarea
            contenteditable="plaintext-only"
            class="discussion-edit-reply-text-area"
            v-model="editReplyContent"
            data-test="discussion-reply-edit-text-area"
          />
          <div class="discussion-reply-actions">
            <button
              class="secondary-button"
              @click="cancelEditReply"
              data-test="edit-discussion-reply-cancel"
            >
              Cancel
            </button>
            <button
              class="primary-button save-button"
              @click="confirmEditReply"
              data-test="edit-discussion-reply-save"
            >
              Save
            </button>
          </div>
        </div>
      </div>
    </blockquote>
  </div>
</template>

<script setup>
import {computed, ref} from 'vue';
import ContextMenu from '@/components/ContextMenu.vue';

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


const editReplyContent = ref(props.content);
const editingReplyFlag = ref(false);

// computed

const timestamp = computed(() => {
  return new Date(props.publishTimestamp + 'Z').toLocaleString();
});

const isUser = computed(() => {
  return props.userClientId == props.authorId;
});

// functions

function editDiscussionReply() {
  editingReplyFlag.value = ref(true);
}

function confirmEditReply() {
  editingReplyFlag.value = ref(false);
  emit('reply:edit', props.replyId, editReplyContent.value);
}

function cancelEditReply() {
  editingReplyFlag.value = ref(false);
  editReplyContent.value = props.content;
}

function deleteDiscussionReply(replyId) {
  emit('reply:delete', replyId);
}

</script>

<style scoped>

.discussion-reply {
  border-radius: var(--content-border-radius);
  padding: var(--p-10);
  background-color: var(--rosalution-grey-50);
  margin-left: var(--p-8);
}

.discussion-reply-header {
  display: flex;
  justify-content: space-between;
  min-height: 2.5rem;
}

/* .discussion-reply-content {
  margin-bottom: var(--p-10);
} */

.discussion-reply-quote {
  border-left: var(--p-5) solid var(--rosalution-grey-50);
  /* padding-right: var(--p-8); */
}

.context-menu {
 display:flex;
 flex-wrap: nowrap;
 justify-content: right;
 /* margin-right: var(--p-10); */
}

.header-icon {
  color: var(--rosalution-purple-300);
  cursor: pointer;
  padding: var(--p-5)
}

.save-button {
  margin-left: var(--p-8);
}

.discussion-edit-reply {
  background-color: var(--rosalution-grey-000);
  border-radius: var(--content-border-radius);
  margin-top: var(--p-8);
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.discussion-edit-reply-text-area {
  background-color: var(--rosalution-white);
  border-radius: var(--content-border-radius);
  margin-top: var(--p-8);
  margin-bottom: var(--p-8);
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.discussion-reply-actions {
  width: 100%;
  display: flex;
  justify-content: right;
  margin-right: var(--p-16);
  margin-bottom: var(--p-10);
}

</style>
