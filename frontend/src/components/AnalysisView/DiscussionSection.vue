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
                >
                  Attach
                </button>
                <div class="new-attachments-list">
                  <span class="new-attachment" v-for="newAttachment, index in newAttachments"
                  v-bind:key="index">
                    <span class="new-attachment-logo">
                      <font-awesome-icon :icon="['far', 'file']" size="lg" v-if="newAttachment.type==='file'"/>
                      <font-awesome-icon icon="link" size="lg" v-else-if="newAttachment.type==='link'"/>
                    </span>
                    <span class="new-attachment-name">
                      {{ newAttachment.name }}
                    </span>
                    <font-awesome-icon icon="xmark" size="md" @click="removePostAttachment('new_post', newAttachment)"/>
                  </span>
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
import notificationDialog from '@/notificationDialog.js';

import inputDialog from '@/inputDialog.js';
import {toRaw} from 'vue';

export default {
  name: 'discussion-section',
  emits: ['discussion:new-post', 'discussion:edit-post', 'discussion:delete-post', 'discussion:open-modal'],
  components: {
    DiscussionPost,
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

      // const defaultComments = 'This attachment is referenced in the Discussion attachment.';
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
    async removePostAttachment(postId, postAttachment) {
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

      try {
        const attachmentIndex = this.newAttachments.findIndex((attachment) => {
          if ('attachment_id' in postAttachment && 'attachment_id' in attachment) {
            return postAttachment.attachment_id == attachment.attachment_id;
          }

          return postAttachment.name == attachment.name;
        });
        console.log(`${attachmentIndex} - attachment to remove`);

        this.newAttachments.splice(attachmentIndex, 1);
      } catch (error) {
        await notificationDialog.title('Failure').confirmText('Ok').alert(error);
      }
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
background-color:   var(--rosalution-grey-300);
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

.attachment {
background-color: var(--rosalution-white);
color: var(--rosalution-black);
border-radius: var(--content-border-radius);
border: 1px solid var(--rosalution-black);

display: flex;
gap: var(--p-5);
align-items: center;
}

.attachment-icon {
padding: var(--p-1);
cursor: pointer;
}

.remove-attachment-icon {
padding-left: var(--p-1);
}

.remove-attachment-icon:hover {
color: var(--rosalution-grey-300)
}

.collapsable-icon {
  color: var(--rosalution-grey-200);
  cursor: pointer;
}

input[type="checkbox"] {
  display: none;
}

<<<<<<< HEAD
.rosalution-section-container input[type="checkbox"]:checked ~ .discussion-section-content {
    display: none;
=======
.rosalution-section-container input[type="checkbox"]:checked ~ .section-content {
  display: none;
>>>>>>> cbecc21 (Added Angelina's code for deleting Discussion attachments. Also, pushing up code for sending attachments to the backend. Will be cleaning that up completely, commiting for reference.)
}

input[type="checkbox"]:checked ~ .rosalution-section-header > span ~ label.collapsable-icon {
  transform: scaleY(-1);
}
</style>
