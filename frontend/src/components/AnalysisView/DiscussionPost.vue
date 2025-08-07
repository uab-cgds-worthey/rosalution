<template>
<div class="discussion-post-container">
  <div class="discussion-post" data-test="discussion-post">
      <div class="discussion-header" data-test="discussion-post-header">
        <div>
          <b>{{ authorName }}</b>
          {{  timestamp  }}
        </div>
        <ul v-if="isUser" class="context-menu" data-test="discussion-post-context-menu">
          <ContextMenu
            :actions="actions"
            :contextId="id"
            @edit="editPost"
            @delete="deletePost"
            >
            <font-awesome-icon class="header-icon" icon="ellipsis-vertical" size="xl" />
          </ContextMenu>
        </ul>
      </div>
      <div class="discussion-body">
        <div v-if="!editingPostFlag" class="discussion-content" data-test="discussion-post-content">
          <span v-for="(rowContent, index) in content" :key="index" data-test="value-row">
            {{ rowContent }}
          </span>
          </div>
          <div v-else class="discussion-edit-post">
            <MultilineEditableTextarea
              class="discussion-edit-post-text-area"
              v-model:content="editPostContent"
              data-test="edit-discussion-input"
            />
            <div class="discussion-actions">
              <button
                class="secondary-button"
                @click="cancelEditPost"
                data-test="edit-discussion-cancel"
              >
                Cancel
              </button>
              <button
                class="primary-button save-button"
                @click="confirmEditPost"
                data-test="edit-discussion-save"
              >
                Save
              </button>
            </div>
        </div>
        <div class="discussion-attachment-reply-button-row">
          <div v-if="attachments.length" class="attachments-list" data-test="discussion-attachment">
            <DiscussionAttachment
              v-for="attachment, index in attachments"
              v-bind:key="index"
              postId="new-post"
              :name="attachment.name"
              :type="attachment.type"
              :attachment="attachment"
            >
            </DiscussionAttachment>
          </div>
          <button class="discussion-reply-button" @click="newDiscussionReplyForm"
          data-test="discussion-new-reply-button">
            <font-awesome-icon icon="reply" size="lg"/>
          </button>
        </div>
      </div>
  </div>
  <div class="discussion-new-reply" v-if="showNewReply">
      <MultilineEditableTextarea
        class="discussion-new-reply-text-area"
        v-model:content="newReplyContent"
        data-test="discussion-new-reply-text-area"
      />
      <div class="discussion-reply-actions">
        <span class="reply-attachments-actions">
          <button
            class="primary-button attach-button"
            @click="addAttachmentToDiscussionReply"
            data-test="discussion-reply-attachment-button"
          >
            Attach
          </button>
          <div class="new-reply-attachments-list">
            <DiscussionAttachment
              v-for="newReplyAttachment, index in newReplyAttachments"
              v-bind:key="index"
              postId="new-post"
              :name="newReplyAttachment.name"
              :type="newReplyAttachment.type"
              :attachment="newReplyAttachment"
              :removeable="true"
              @remove="removeReplyAttachment('new_reply', index)"
            >
            </DiscussionAttachment>
          </div>
        </span>
        <span class="reply-actions">
          <button
            class="secondary-button"
            @click="cancelNewDiscussionReply"
            data-test="new-discussion-reply-cancel-button"
          >
            Cancel
          </button>
          <button
              class="primary-button"
              @click="newDiscussionReply"
              data-test="discussion-new-reply-publish"
              :disabled="checkReplyContent"
          >
            Publish
          </button>
        </span>
      </div>
  </div>
  <DiscussionReply v-for="reply in thread"
    :replyId="reply.reply_id"
    :key="reply.reply_id"
    :authorId="reply.author_id"
    :authorName="reply.author_fullname"
    :publishTimestamp="reply.publish_timestamp"
    :content="reply.content"
    :userClientId="userClientId"
    :actions="actions"
    @reply:edit="editDiscussionReply"
    @reply:delete="deleteDiscussionReply"
  />
</div>
</template>

<script setup>
import {computed, ref} from 'vue';

import ContextMenu from '@/components/ContextMenu.vue';
import DiscussionAttachment from './DiscussionAttachment.vue';
import DiscussionReply from './DiscussionReply.vue';
import MultilineEditableTextarea from '@/components/AnalysisView/MultilineEditableTextarea.vue';

import notificationDialog from '@/notificationDialog.js';

import inputDialog from '@/inputDialog.js';

import {toRaw} from 'vue';

const emits = defineEmits(['post:edit', 'post:delete', 'discussion:new-reply', 'discussion:edit-reply',
  'discussion:delete-reply']);

const props = defineProps({
  id: {
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
    type: Array,
    default: () => {
      return [];
    },
  },
  attachments: {
    type: Array,
  },
  thread: {
    type: Array,
  },
  existingAttachments: {
    type: Array,
  },
  userClientId: {
    type: String,
  },
  actions: {
    type: Array,
  },
});

const editingPostFlag = ref(false);
const editPostContent = ref(props.content);

const showNewReply = ref(false);

const newReplyContent = defineModel({default: () => []});
const newReplyAttachments = ref([]);

const timestamp = computed(() => {
  return new Date(props.publishTimestamp + 'Z').toLocaleString();
});

const isUser = computed(() => {
  return props.userClientId == props.authorId;
});

const checkReplyContent = computed(() => {
  return newReplyContent.value == '';
});

// -----------------------------------
// Posts
// -----------------------------------

function editPost() {
  editingPostFlag.value = true;
}

function confirmEditPost() {
  editingPostFlag.value = false;
  emits('post:edit', props.id, editPostContent.value);
};

function cancelEditPost() {
  editingPostFlag.value = false;
  editPostContent.value = props.content;
}

function deletePost(postId) {
  emits('post:delete', postId);
}

// -----------------------------------
// Replies
// -----------------------------------

function newDiscussionReplyForm() {
  showNewReply.value = true;
}

function newDiscussionReply() {
  emits('discussion:new-reply', props.id, toRaw(newReplyContent.value));
  clearNewDiscussionReplyField();
}

function cancelNewDiscussionReply() {
  clearNewDiscussionReplyField();
};

function clearNewDiscussionReplyField() {
  newReplyContent.value = [];
  showNewReply.value = false;
  newReplyAttachments.value = [];
};

function editDiscussionReply(replyId, replyContent) {
  emits('discussion:edit-reply', props.id, replyId, replyContent);
};

function deleteDiscussionReply(replyId) {
  emits('discussion:delete-reply', props.id, replyId);
};

async function addAttachmentToDiscussionReply(replyId) {
  const includeComments = false;
  const includeName = true;

  const attachment = await inputDialog
      .confirmText('Attach')
      .cancelText('Cancel')
      .file(includeComments, 'file', '.png, .jpg, .jpeg, .bmp, .png, .gb')
      .url(includeComments, includeName)
      .existing(props.existingAttachments)
      .prompt();
  if (!attachment) {
    return;
  }

  console.log('Received an attachment');
  console.log(attachment);

  if (typeof attachment === 'object' && !Array.isArray(attachment)) {
    newReplyAttachments.value.push(attachment);
  } else {
    for (let i = 0; i < attachment.length; i++) {
      newReplyAttachments.value.push(attachment[i]);
    }
  }
};

async function removeReplyAttachment(replyId, attachmentIndex) {
  const confirmedDelete = await notificationDialog
      .title(`Remove reply attachment?`)
      .confirmText('Remove')
      .cancelText('Cancel')
      .confirm(
          `Remove attachment from new reply. Are you sure you want to remove?`,
      );

  if (!confirmedDelete) {
    return;
  }
  newReplyAttachments.value.splice(attachmentIndex, 1);
}
</script>

<style scoped>
.discussion-post {
  border-radius: var(--content-border-radius);
  padding: var(--p-8);
}

.discussion-post:nth-child(even) {
  background-color: var(--rosalution-grey-50);
}

.discussion-post:nth-child(odd) {
  background-color: var(--rosalution-grey-100);
}

.discussion-header {
  display: flex;
  justify-content: space-between;
  min-height: 2.5rem;
}

.discussion-body {
  display: flex;
  flex-direction: column;
  gap: var(--p-5);
}

.discussion-content {
  display: flex;
  flex-direction: column;
  white-space: pre-wrap;
  margin-bottom: var(--p-10);
}

.fill {
  width: 100%;
}

.context-menu {
 display:flex;
 flex-wrap: nowrap;
 justify-content: right;
 margin-right: var(--p-10);
}

.actions-menu > li {
  float: left;
}

.header-icon {
  color: var(--rosalution-purple-300);
  cursor: pointer;
  padding: var(--p-5)
}

.save-button {
  margin-left: var(--p-8);
}

.discussion-edit-post {
  background-color: var(--rosalution-grey-50);
  border-radius: var(--content-border-radius);
  margin-top: var(--p-8);
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.discussion-edit-post-text-area {
  background-color: var(--rosalution-white);
  border-radius: var(--content-border-radius);
  border: solid;
  border-color: var(--rosalution-grey-000);
  padding: var(--p-16);
  margin: var(--p-10);
  position: relative;
  width: 100%;
}

.discussion-actions {
  width: 100%;
  display: flex;
  justify-content: right;
  margin-right: var(--p-16);
  margin-bottom: var(--p-10);
}

.discussion-attachment-reply-button-row {
  display: flex;
  justify-content: flex-end;
}

.attachments-list {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  grid-auto-rows: auto;
  gap: var(--p-5);
}

.discussion-reply-button {
  border: none;
  background: none;
}

.discussion-new-reply {
  background-color: var(--rosalution-grey-50);
  border-radius: var(--content-border-radius);
  display: flex;
  flex-direction: column;
  gap: var(--p-8);
  padding: var(--p-8);
}

.discussion-new-reply-text-area {
  background-color: var(--rosalution-white);
  border-radius: var(--content-border-radius);
  border: solid;
  border-color: var(--rosalution-grey-000);
  padding: var(--p-16);
}

.discussion-reply-actions {
  display: flex;
  justify-content: space-between;
  gap: var(--p-8);
}

.reply-actions {
  display: flex;
  gap: var(--p-5);
}

.reply-attachments-actions {
  display: flex;
  gap: var(--p-10);
}

.new-reply-attachments-list {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  grid-auto-rows: auto;
  gap: var(--p-5);
}

</style>
