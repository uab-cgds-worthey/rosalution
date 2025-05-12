<template>
  <div class="rosalution-section-container">
    <input type="checkbox" id="discussion_toggle" />
    <div class="rosalution-section-header">
        <h2 class="rosalution-section-header-text">Discussion</h2>
        <span class="rosalution-section-center"></span>
        <button
            class="primary-button discussion-new-button"
            @click="this.newDiscussionPostForm"
            data-test="new-discussion-button"
        >
          New Discussion
        </button>
        <label class="collapsable-icon" for="discussion_toggle">
            <font-awesome-icon icon="chevron-down" size="lg"/>
        </label>
    </div>
    <div class="rosalution-section-seperator"></div>
    <div class="discussion-section-content">
      <div v-if="this.showNewPost" class="discussion-new-post">
        <textarea
            contenteditable="plaintext-only"
            class="discussion-new-post-text-area"
            v-model="newPostContent"
            data-test="new-discussion-input"
        />
        <div class="discussion-actions">
          <span class="attachments-actions">
            <button
              class="primary-button attach-button"
              @click="addAttachmentToDiscussionPost"
              data-test="discussion-attachment-button"
            >
              Attach
            </button>
            <div class="attachments-list">
              <DiscussionAttachment
                v-for="newAttachment, index in newAttachments"
                v-bind:key="index"
                postId="new-post"
                :name="newAttachment.name"
                :type="newAttachment.type"
                :attachment="newAttachment"
                :removeable="true"
                @remove="removePostAttachment('new_post', index)"
              >
              </DiscussionAttachment>
            </div>
          </span>
          <span class="post-actions">
            <button
              class="secondary-button"
              @click="cancelNewDiscussionPost"
              data-test="new-discussion-cancel"
            >
              Cancel
            </button>
            <button
                class="primary-button publish-button"
                @click="newDiscussionPost"
                data-test="new-discussion-publish"
                :disabled="this.checkPostContent"
            >
              Publish
            </button>
          </span>
        </div>
      </div>
      <DiscussionPost v-for="discussion in discussions"
          :id="discussion.post_id"
          :key="discussion.post_id"
          :authorId="discussion.author_id"
          :authorName="discussion.author_fullname"
          :publishTimestamp="discussion.publish_timestamp"
          :content="discussion.content"
          :attachments="discussion.attachments"
          :thread="discussion.thread"
          :userClientId="userClientId"
          :actions="actions"
          @post:edit="this.editDiscussionPost"
          @post:delete="this.deleteDiscussionPost"
          @discussion:new-reply="this.addDiscussionReply"
          @discussion:edit-reply="this.editDiscussionReply"
          @discussion:delete-reply="this.deleteDiscussionReply"
      />
    </div>
  </div>
</template>

<script>
import DiscussionPost from './DiscussionPost.vue';
import DiscussionAttachment from './DiscussionAttachment.vue';

import notificationDialog from '@/notificationDialog.js';

import inputDialog from '@/inputDialog.js';
import {toRaw} from 'vue';

export default {
  name: 'discussion-section',
  emits: ['discussion:new-post', 'discussion:edit-post', 'discussion:delete-post', 'discussion:open-modal',
    'discussion:new-reply', 'discussion:edit-reply', 'discussion:delete-reply'],
  components: {
    DiscussionPost,
    DiscussionAttachment,
  },
  props: {
    header: {
      type: String,
    },
    discussions: {
      type: Array,
    },
    userClientId: {
      type: String,
    },
    actions: {
      type: Array,
    },
    existingAttachments: {
      type: Array,
    },
  },
  data: function() {
    return {
      newPostContent: '',
      showNewPost: false,
      newAttachments: [],
    };
  },
  computed: {
    checkPostContent() {
      return this.newPostContent == '';
    },
  },
  methods: {
    newDiscussionPostForm() {
      this.showNewPost = true;
    },
    newDiscussionPost() {
      this.$emit('discussion:new-post', toRaw(this.newPostContent), toRaw(this.newAttachments));
      this.clearNewDiscussionField();
    },
    cancelNewDiscussionPost() {
      this.clearNewDiscussionField();
    },
    clearNewDiscussionField() {
      this.newPostContent = '';
      this.showNewPost = false;
      this.newAttachments = [];
    },
    editDiscussionPost(postId, postContent) {
      this.$emit('discussion:edit-post', postId, postContent);
    },
    deleteDiscussionPost(postId) {
      this.$emit('discussion:delete-post', postId);
    },
    async addAttachmentToDiscussionPost(postId) {
      const includeComments = false;
      const includeName = true;

      const attachment = await inputDialog
          .confirmText('Attach')
          .cancelText('Cancel')
          .file(includeComments, 'file', '.png, .jpg, .jpeg, .bmp, .png, .gb')
          .url(includeComments, includeName)
          .existing(this.existingAttachments)
          .prompt();
      if (!attachment) {
        return;
      }

      if (typeof attachment === 'object' && !Array.isArray(attachment)) {
        this.newAttachments.push(attachment);
      } else {
        for (let i = 0; i < attachment.length; i++) {
          this.newAttachments.push(attachment[i]);
        }
      }
    },
    async removePostAttachment(postId, attachmentIndex) {
      const confirmedDelete = await notificationDialog
          .title(`Remove post attachment?`)
          .confirmText('Remove')
          .cancelText('Cancel')
          .confirm(
              `Remove attachment from new post. Are you want to remove?`,
          );

      if (!confirmedDelete) {
        return;
      }
      this.newAttachments.splice(attachmentIndex, 1);
    },
    addDiscussionReply(postId, newReplyContent) {
      this.$emit('discussion:new-reply', postId, toRaw(newReplyContent));
    },
    editDiscussionReply(postId, replyId, replyContent) {
      this.$emit('discussion:edit-reply', postId, replyId, replyContent);
    },
    deleteDiscussionReply(postId, replyId) {
      this.$emit('discussion:delete-reply', postId, replyId);
    },
  },
};

</script>

<style scoped>
.rosalution-section-seperator {
  margin: var(--p-8) 0
}

.discussion-section-content {
  display: flex;
  flex-direction: column;
  gap: var(--p-10);
}

.discussion-new-post {
  background-color: var(--rosalution-grey-50);
  border-radius: var(--content-border-radius);
  display: flex;
  flex-direction: column;
  gap: var(--p-8);
  padding: var(--p-8);
}

.discussion-new-post-text-area {
  background-color: var(--rosalution-white);
  border-radius: var(--content-border-radius);
  border: solid;
  border-color: var(--rosalution-grey-000);
  padding: var(--p-16);
}

.discussion-actions {
  display: flex;
  justify-content: space-between;
  gap:var(--p-8);
}

.post-actions {
  display: flex;
  gap: var(--p-5);
}

.attachments-actions {
  display: flex;
  gap: var(--p-10);
}

.attachments-list {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  grid-auto-rows: auto;
  gap: var(--p-5);
}

.collapsable-icon {
  color: var(--rosalution-grey-200);
  cursor: pointer;
}

input[type="checkbox"] {
  display: none;
}

.rosalution-section-container input[type="checkbox"]:checked ~ .discussion-section-content {
    display: none;
}

input[type="checkbox"]:checked ~ .rosalution-section-header > span ~ label.collapsable-icon {
  transform: scaleY(-1);
}
</style>
