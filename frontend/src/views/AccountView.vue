<template>
  <div>
    <app-header>
      <Header :username="user.username">
      <span class="empty-fill"></span>
      </Header>
    </app-header>
    <app-content>
      User Information
      <p>{{ user }}</p>
      <button @click="generateSecret" type="submit">
          Generate Secret
      </button>
    </app-content>
  </div>
</template>

<script>
import {authStore} from '../stores/authStore';

import Header from '../components/Header.vue';

export default {
  name: 'account-view-component',
  components: {
    Header,
  },
  computed: {
    user() {
      return authStore.getUser();
    },
  },
  methods: {
    async generateSecret() {
      const userObject = await authStore.generateSecret();
      console.log(userObject);
    },
  },
};
</script>

<style>
.empty-fill {
  flex: 1 1 auto;
  display: inline-flex;
}
</style>
