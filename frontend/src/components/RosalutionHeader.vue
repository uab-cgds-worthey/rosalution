<template>
  <header>
    <router-link :to="{path: '/rosalution/'}">
      <img src="@/assets/rosalution-logo.svg" class="rosalution-logo">
    </router-link>
    <div data-test="primary-content" class="content">
      <router-link v-if="doTitleToRoute" :to="titleToRoute" class="title left-content">
        {{ titleText }}
      </router-link>
      <a v-else class="title left-content" href="#top" data-test="header-title-text">{{ titleText }}</a>
      <slot></slot>
      <ul class="actions-menu">
        <drop-down-menu :actions="this.userAuthActions" data-test="auth-menu">
          <span v-if="username" class="login" data-test="user-text">
            {{ username }}
          </span>
          <font-awesome-icon class="header-icon" icon="user-doctor" size="xl" />
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
  },
  computed: {
    actionsExist: function() {
      return this.actions.length !== 0;
    },
    doTitleToRoute: function() {
      return typeof(this.titleToRoute) !== 'undefined';
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
  gap: 12px;
  padding: var(--p-8);
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
