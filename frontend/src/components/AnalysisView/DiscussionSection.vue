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
              <button
                  class="primary-button attach-button"
                  @click="addAttachmentToDiscussionPost"
              >
                Attach
              </button>
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

export default {
  name: 'discussion-section',
  emits: ['discussion:new-post', 'discussion:edit-post', 'discussion:delete-post'],
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
  },
  data: function() {
    return {
      newPostContent: '',
      showNewPost: false,
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
      this.$emit('discussion:new-post', this.newPostContent);
      this.clearNewDiscussionField();
    },
    cancelNewDiscussionPost() {
      this.clearNewDiscussionField();
    },
    clearNewDiscussionField() {
      this.newPostContent = '';
      this.showNewPost = false;
    },
    editDiscussionPost(postId, postContent) {
      this.$emit('discussion:edit-post', postId, postContent);
    },
    deleteDiscussionPost(postId) {
      this.$emit('discussion:delete-post', postId);
    },
    addAttachmentToDiscussionPost() {

    }
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
    justify-content: right;
    margin-right: var(--p-16);
    margin-bottom: var(--p-10);
}

.publish-button {
    margin-left: var(--p-8);
}

.attach-button {
  background-color:   var(--rosalution-grey-300);
  color: var(--rosalution-black)
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
