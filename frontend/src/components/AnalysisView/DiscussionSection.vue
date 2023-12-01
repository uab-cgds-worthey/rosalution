<template>
    <div class="rosalution-section-container">
        <input type="checkbox" id="discussion_toggle" />
        <div class="rosalution-section-header">
            <h2 class="rosalution-section-header-text">Discussion</h2>
            <span class="rosalution-section-center" data-test="header-datasets"/>
            <button class="primary-button discussion-new-button" @click="this.newDiscussionPost">New Discussion</button>
            <label class="collapsable-icon" for="discussion_toggle">
                <font-awesome-icon icon="chevron-down" size="lg"/>
            </label>
        </div>
        <div class="rosalution-section-seperator"></div>
        <div class="section-content">
            <div class="discussion-new-post">
                <textarea
                    contenteditable="plaintext-only"
                    class="discussion-new-post-text-area"
                    v-model="newPostContent"
                    data-test="new-discussion-input"
                />
                <div class="discussion-actions">
                    <button class="secondary-button" @click="cancelNewDiscussionPost" data-test="new-discussion-cancel">
                        Cancel
                    </button>
                    <button class="primary-button" @click="newDiscussionPost" data-test="new-discussion-publish">
                        Publish
                    </button>
                </div>
            </div>
            <DiscussionPost v-for="discussion in discussions"
                :id="discussion.post_id"
                :key="discussion.post_id"
                :author_id="discussion.author_id"
                :author_name="discussion.author_fullname"
                :publish_timestamp="discussion.publish_timestamp"
                :content="discussion.content"
                :attachments="discussion.attachments"
                :thread="discussion.thread"
            />
        </div>
    </div>
</template>

<script>
import DiscussionPost from './DiscussionPost.vue';

export default {
  name: 'discussion-section',
  emits: ['discussion:new-post'],
  components: {
    DiscussionPost,
  },
  props: {
    header: {
      type: String,
    },
    discussions: {
      type: Array,
      default: () => {
        return [];
      },
    },
  },
  data: function() {
    return {
      newPostContent: '',
    };
  },
  methods: {
    newDiscussionPost() {
      this.$emit('discussion:new-post', this.newPostContent);
    },
    cancelNewDiscussionPost() {
      // Currently does nothing, will need to update to turn off the new post text
      console.log('Cancelled post');
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
    justify-content: right;
    margin-right: var(--p-16);
}

.collapsable-icon {
    color: var(--rosalution-grey-200);
    cursor: pointer;
}

input[type="checkbox"] {
    display: none;
}

.rosalution-section-container input[type="checkbox"]:checked ~ .section-content {
    display: none;
}

input[type="checkbox"]:checked ~ .rosalution-section-header > span ~ label.collapsable-icon {
    transform: scaleY(-1);
}
</style>
