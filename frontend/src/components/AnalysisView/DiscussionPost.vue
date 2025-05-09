<template>
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
            @edit="this.editPost"
            @delete="this.deletePost"
            >
            <font-awesome-icon class="header-icon" icon="ellipsis-vertical" size="xl" />
          </ContextMenu>
        </ul>
      </div>
      <div v-if="!editingPostFlag" class="discussion-content" data-test="discussion-post-content">
          {{ content }}
      </div>
      <div v-else class="discussion-edit-post">
        <textarea
          contenteditable="plaintext-only"
          class="discussion-edit-post-text-area"
          v-model="editPostContent"
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
    <div v-if="attachments.length" class="attachments-list">
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
  </div>
</template>

<script>
import ContextMenu from '@/components/ContextMenu.vue';
import DiscussionAttachment from './DiscussionAttachment.vue';

export default {
  name: 'discussion-post',
  emits: ['post:edit', 'post:delete', 'attachment:download'],
  components: {
    ContextMenu,
    DiscussionAttachment,
  },
  props: {
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
      type: String,
    },
    attachments: {
      type: Array,
    },
    existingAttachment: {
      type: Array,
    },
    thread: {
      type: Array,
    },
    userClientId: {
      type: String,
    },
    actions: {
      type: Array,
    },
  },
  data: function() {
    return {
      editingPostFlag: false,
      editPostContent: this.content,
    };
  },
  computed: {
    timestamp: function() {
      return new Date(this.publishTimestamp + 'Z').toLocaleString();
    },
    isUser: function() {
      return this.userClientId == this.authorId;
    },
  },
  methods: {
    editPost() {
      this.editingPostFlag = true;
    },
    confirmEditPost() {
      this.editingPostFlag = false;
      this.$emit('post:edit', this.id, this.editPostContent);
    },
    cancelEditPost() {
      this.editingPostFlag = false;
      this.editPostContent = this.content;
    },
    deletePost(postId) {
      this.$emit('post:delete', postId);
    },
  },
};
</script>

<style scoped>
.discussion-post {
  border-radius: var(--content-border-radius);
  padding: var(--p-8);
  margin-top: var(--p-10);
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
  margin-top: var(--p-5);
  margin-bottom: var(--p-5);
}

.discussion-content {
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

.attachments-list {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  grid-auto-rows: auto;
  gap: var(--p-5);
}


</style>
