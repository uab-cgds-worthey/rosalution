<template>
    <div class="discussion-post" data-test="discussion-post">
        <div class="discussion-header" data-test="discussion-post-header">
          <div>
            <b>{{ author_name }}</b>
            {{  timestamp  }}
          </div>
          <ul v-if="isUser" class="actions-menu">
            <!-- <DropDownMenu :actions="this.postActions">
              <font-awesome-icon class="header-icon" icon="caret-down" size="xl" />
            </DropDownMenu> -->
            <ContextMenu :actions="this.postActions" :context_id="id">
              <font-awesome-icon class="header-icon" icon="caret-down" size="xl" />
            </ContextMenu>
          </ul>
        </div>
        <div class="discussion-content" data-test="discussion-post-content">
            {{ content }}
        </div>
    </div>
</template>

<script>
import DropDownMenu from '@/components/DropDownMenu.vue';
import ContextMenu from '@/components/ContextMenu.vue';

export default {
  name: 'discussion-post',
  components: {
    DropDownMenu,
    ContextMenu
  },
  props: {
    id: {
      type: String,
    },
    author_id: {
      type: String,
    },
    author_name: {
      type: String,
    },
    publish_timestamp: {
      type: String,
    },
    content: {
      type: String,
    },
    attachments: {
      type: Array,
      default: () => {
        return [];
      },
    },
    thread: {
      type: Array,
      default: () => {
        return [];
      },
    },
    userClientId: {
      type: String
    }
  },
  data: function() {
    return {
      postActions: [
        {
          icon: 'pencil',
          text: 'Edit',
          operation: () => {
            console.log("Editing post")
          },
        },
        {
          divider: true
        },
        {
          icon: 'xmark',
          text: 'Delete',
          operation: () => {
            console.log("Deleting post")
          },
        },
      ]
    }
  },
  computed: {
    timestamp: function() {
      return new Date(this.publish_timestamp).toUTCString();
    },
    isUser: function() {
      return this.userClientId == this.author_id
    }
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

.actions-menu {
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
}

</style>
