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
              @delete="this.deletePost"
              >
              <font-awesome-icon class="header-icon" icon="ellipsis-vertical" size="xl" />
            </ContextMenu>
          </ul>
        </div>
        <div class="discussion-content" data-test="discussion-post-content">
            {{ content }}
        </div>
    </div>
</template>

<script>
import ContextMenu from '@/components/ContextMenu.vue';

export default {
  name: 'discussion-post',
  emits: ['post:delete'],
  components: {
    ContextMenu,
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
  computed: {
    timestamp: function() {
      return new Date(this.publishTimestamp).toUTCString();
    },
    isUser: function() {
      return this.userClientId == this.authorId;
    },
  },
  methods: {
    deletePost(postId) {
      this.$emit('post:delete', postId);
    },
  },
  methods: {
    deletePost(post_id) {
      this.$emit('post:delete', post_id);
    }
  }
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

</style>
