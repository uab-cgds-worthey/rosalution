<template>
  <header>
    <router-link :to="{path: '/rosalution/'}">
      <img src="@/assets/rosalution-logo.svg" class="rosalution-logo">
    </router-link>
    <div data-test="primary-content" class="content">
      <a class="title left-content" href="#top" data-test="header-title-text">{{ titleText }}</a>
      <slot>
      </slot>
      <router-link to="/rosalution/login">
        <span v-if="username" class="login" data-test="user-text">{{ username }}</span>
      </router-link>
      <router-link to="/rosalution/login">
        <button class="login" data-test="user-menu">
          <font-awesome-icon class="header-icon" icon="user-doctor" size="xl"/>
        </button>
      </router-link>
      <font-awesome-icon v-if="actionsExist" class="header-icon" icon="ellipsis-vertical" size="xl"/>
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
  color: var(--rosalution-purple-300)
}

a:active.title.left-content {
  color: var(--rosalution-purple-200)
}

a:visited.title.left-content {
  color: var(--rosalution-purple-300)
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
  border: none;
  background-color: white;
  font-size: 1.125rem;
  line-height: 2rem;
  cursor: pointer;
}

.header-icon {
  color: var(--rosalution-purple-300);
}

</style>
