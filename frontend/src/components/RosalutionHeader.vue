<template>
  <header>
    <router-link :to="{path: '/rosalution/'}">
      <img src="@/assets/rosalution-logo.svg" class="rosalution-logo">
    </router-link>
    <div data-test="primary-content" class="content">
      <a v-if="this.workflow_status !== 'none'" class="status-icon" data-test="status-icon">
          <font-awesome-icon :icon="workflowIcon" size="xl" :style="workflowColorStyle"/>
      </a>
      <router-link v-if="doTitleToRoute" :to="titleToRoute" class="title left-content">
        {{ titleText }}
      </router-link>
      <a v-else class="title left-content" href="#top" data-test="header-title-text">{{ titleText }}</a>
      <a
        v-for="link in third_party_links"
        :key="link.type"
        :href="link.link"
        target="_blank"
        class="third-party-logo-link"
        data-test="third-party-link"
        rel="noopener noreferrer"
      >
        <img :src="getIconSrc(link.type)" :class="getIconClass(link.type)" />
      </a>
      <slot></slot>
      <ul class="actions-menu">
        <drop-down-menu :actions="this.userAuthActions" data-test="auth-menu">
          <router-link :to="{path: '/rosalution/account'}" class="auth-menu">
            <span v-if="username" class="login" data-test="user-text">
              {{ username }}
            </span>
            <font-awesome-icon class="header-icon" icon="user-doctor" size="xl" />
          </router-link>
        </drop-down-menu>
        <drop-down-menu v-if="actionsExist" :actions="actions" data-test="user-menu">
          <font-awesome-icon class="header-icon" icon="bars" size="xl" />
        </drop-down-menu>
      </ul>
    </div>
  </header>
</template>

<script>
import DropDownMenu from '@/components/DropDownMenu.vue';
import {StatusType} from '@/config.js';

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
    workflow_status: {
      type: String,
      default: 'none',
    },
    third_party_links: {
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
    workflowIcon: function() {
      if ( !(this.workflow_status in StatusType) ) {
        return 'question';
      }

      return StatusType[this.workflow_status].icon;
    },
    workflowColor: function() {
      if ( !(this.workflow_status in StatusType) ) {
        return '--rosalution-white';
      }

      return StatusType[this.workflow_status].color;
    },
    workflowColorStyle: function() {
      return {
        color: `var(${this.workflowColor})`,
      };
    },
  },
  methods: {
    getIconSrc(linkType) {
      if (linkType === 'monday_com') {
        return new URL('/src/assets/monday-avatar-logo.svg', import.meta.url);
      } else if (linkType === 'phenotips_com') {
        return new URL('/src/assets/phenotips-favicon-96x96.png', import.meta.url);
      }
    },
    getIconClass(linkType) {
      if (linkType === 'monday_com') {
        return 'monday-icon';
      } else if (linkType === 'phenotips_com') {
        return 'phenotips-icon';
      }
    },
  },
};
</script>

<style scoped>
header {
  display: flex;
  flex-direction: row;
  gap: var(--p-16);
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
  white-space: nowrap;
}

.header-icon {
  color: var(--rosalution-purple-300);
  padding: var(--p-8);
}

.actions-menu {
 display:flex;
 flex-wrap: nowrap;
}

.actions-menu > li {
  float: left;
}
.status-icon {
  transform: translateX(6px);
}

.third-party-logo-link {
  background-color: transparent;
  padding: 0;
  transform: translate(0, 4px);
}

.monday-icon {
  width: 1.875rem; /* 30px */
  height: 1.875rem; /* 30px */
  transform: translate(-8px, 0);
}

.phenotips-icon {
  width: 1.25rem; /* 20px */
  height: 1.25rem; /* 20px */
  transform: translate(-16px, 0);
}

.auth-menu {
  display:flex;
  align-items: center;
}

</style>
