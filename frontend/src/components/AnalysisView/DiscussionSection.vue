<template>
  <div class="rosalution-section-container">
    <input type="checkbox" id="discussion_toggle" />
    <div class="rosalution-section-header">
        <h2 class="rosalution-section-header-text">Discussion</h2>
        <span class="rosalution-section-center" data-test="header-datasets"/>
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
  emits: ['discussion:new-post', 'discussion:edit-post', 'discussion:delete-post', 'discussion:open-modal'],
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
      const postAttachment = this.newAttachments[attachmentIndex];
      const confirmedDelete = await notificationDialog
          .title(`Remove '${postAttachment.name}' attachment from post?`)
          .confirmText('Remove')
          .cancelText('Cancel')
          .confirm(
              'This operation will  sure you want to remove?',
          );

      if (!confirmedDelete) {
        return;
      }
      this.newAttachments.splice(attachmentIndex, 1);
    },
  },
};

</script>

<style scoped>
.discussion-new-button {
  margin-bottom: var(--p-8);
  margin-right: var(--p-8);
}

.discussion-new-post {
  background-color: var(--rosalution-grey-50);
  border-radius: var(--content-border-radius);
  margin-top: var(--p-8);
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.discussion-new-post-text-area {
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
  justify-content: space-between;
  flex-wrap: wrap;
  margin-right: var(--p-16);
  margin-bottom: var(--p-10);
}

.post-actions {
  display: flex;
  flex-wrap: wrap;
}

.publish-button {
  margin-left: var(--p-8);
}

.attachments-actions {
  display: flex;
  flex-wrap: wrap;
}

.attach-button {
  background-color: var(--rosalution-grey-300);
  color: var(--rosalution-black);
  margin-left: var(--p-16);
  margin-right: var(--p-10);
  left: var(--p-28);
  float: left;
}

.attachments-list {
  display: flex;
  align-items: center;
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
