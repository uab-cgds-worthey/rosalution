<template>
  <header>
    <router-link :to="{path: '/rosalution/'}">
      <img src="@/assets/rosalution-logo.svg" class="rosalution-logo">
    </router-link>
    <div data-test="primary-content" class="content">
      <!--todo: verify with team to disable the link 'visited' style from the title -->
      <!--todo: ask what the acitve styling should be again for a hyperlink, chose the 200 purple for now-->
      <router-link class="title left-content" :to="titleRouteParams" data-test="header-title-text">
        {{ titleText }}
      </router-link>
      <slot>
      </slot>
      <span v-if="username" class="login" data-test="user-text">{{ username }}</span>
      <router-link to="/rosalution/login">
        <button class="login" data-test="user-menu">LOGIN</button>
      </router-link>
      <font-awesome-icon v-if="actionsExist" icon="ellipsis-vertical" size="xl"></font-awesome-icon>
    </div>
  </header>
</template>

<script>
export default {
  name: 'header-component',
  props: {
    titleText: {
      type: String,
      default: 'rosalution',
    },
    titleRouteParams: {
      type: Object,
      default: () => {
        return {
          path: '/rosalution/',
        };
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
  },
};
</script>

<style>
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

/** todo: need to figure out what this style ought to be */
.login {
  font-size: 1.125rem;
  line-height: 2rem;
}

</style>
