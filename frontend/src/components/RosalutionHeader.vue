<template>
  <header>
    <router-link :to="{path: '/rosalution/'}">
      <img src="@/assets/rosalution-logo.svg" class="rosalution-logo">
    </router-link>
    <div data-test="primary-content" class="content">
      <a v-if="this.workflow_status" class="status-icon" :class="status" data-test="status-icon">
          <font-awesome-icon :icon="workflowIcon" size="xl" :style="workflowColorStyle"/>
      </a>
      <router-link v-if="doTitleToRoute" :to="titleToRoute" class="title left-content">
        {{ titleText }}
      </router-link>
      <a v-else class="title left-content" href="#top" data-test="header-title-text">{{ titleText }}</a>
      <slot></slot>
      <ul class="actions-menu">
        <drop-down-menu :actions="this.userAuthActions" data-test="auth-menu">
          <router-link :to="{path: '/rosalution/account'}">
            <span v-if="username" class="login" data-test="user-text">
              {{ username }}
            </span>
            <font-awesome-icon class="header-icon" icon="user-doctor" size="xl" />
          </router-link>
        </drop-down-menu>
        <drop-down-menu v-if="actionsExist" :actions="actions" data-test="user-menu">
          <font-awesome-icon class="header-icon" icon="ellipsis-vertical" size="xl" />
        </drop-down-menu>
      </ul>
    </div>
  </header>
</template>

<script>
import DropDownMenu from '@/components/DropDownMenu.vue';

export default {
  name: 'rosalution-header-component',
  components: {
    DropDownMenu,
  },
  data: function() {
    return {
      userAuthActions: [{
        icon: '',
        text: 'Logout',
        operation: () => {
          this.$emit('logout');
        },
      }],
    };
  },
  props: {
    titleText: {
      type: String,
      default: 'rosalution',
    },
    titleToRoute: {
      type: Object,
      default: () => {
        return undefined;
      },
    },
    username: String,
    actions: {
      type: Array,
      default: () => {
        return [];
      },
    },
    workflow_status : {
      type: String,
      default: 'none',
    },
  },
  computed: {
    actionsExist: function() {
      return this.actions.length !== 0;
    },
    doTitleToRoute: function() {
      return typeof(this.titleToRoute) !== 'undefined';
    },
    workflowIcon: function () {
      if (this.workflow_status == 'Annotation') {
        return 'asterisk';
      } else if (this.workflow_status == 'Ready') {
        return 'clipboard-check';
      } else if (this.workflow_status == 'Active') {
        return 'book-open';
      } else if (this.workflow_status == 'Approved') {
        return 'check';
      } else if (this.workflow_status == 'On-Hold') {
        return 'pause';
      } else if (this.workflow_status == 'Declined') {
        return 'x';
      }

      return 'question';
    },
    workflowColor: function () {
      if (this.workflow_status == 'Annotation') {
        return '--rosalution-status-annotation';
      } else if (this.workflow_status == 'Ready') {
        return '--rosalution-status-ready';
      } else if (this.workflow_status == 'Active') {
        return '--rosalution-status-active';
      } else if (this.workflow_status == 'Approved') {
        return '--rosalution-status-approved';
      } else if (this.workflow_status == 'On-Hold') {
        return '--rosalution-status-on-hold';
      } else if (this.workflow_status == 'Declined') {
        return '--rosalution-status-declined';
      }

      return '--rosalution-white';
    },
    workflowColorStyle: function () {
      return {
        color: `var(${this.workflowColor})`,
      };
    },
  },
};
</script>

<style scoped>
header {
  display: flex;
  flex-direction: row;
  gap: 15px;
  background-color: var(--primary-background-color);
}

img.rosalution-logo {
  width: 55px;
  height: 45px;
  flex: 0 0 auto;
}

a:link.title.left-content {
  color: var(--rosalution-purple-300);
}

a:active.title.left-content {
  color: var(--rosalution-purple-200);
}

a:visited.title.left-content {
  color: var(--rosalution-purple-300);
}

header .content {
  display: flex;
  flex: 1 1 auto;
  align-items: center;
  padding: var(--p-8);
  gap: 12px;
  border-radius: var(--content-border-radius);
  background-color: var(--secondary-background-color);
}

header .left-content {
  flex: 0;
}

.login {
  border: none;
  background-color: white;
  font-size: 1.125rem;
  line-height: 2rem;
  cursor: pointer;
  color: var(--rosalution-purple-300);
  font-weight: 600;
  vertical-align: super;
}

.header-icon {
  color: var(--rosalution-purple-300);
  padding: var(--p-8);
}

.actions-menu > li {
  float: left;
}
</style>
