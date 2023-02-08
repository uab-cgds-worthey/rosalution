<template>
  <div>
    <app-header>
      <Header :username="user.username">
      <span class="empty-fill"></span>
      </Header>
    </app-header>
    <app-content>
      <SectionBox
        :header="'User'"
        :content="[
          {field: 'Username', value: [user.username]},
          {field: 'Full Name', value: [user.full_name]},
          {field: 'Email', value: [user.email]},
        ]"
      />
      <SectionBox
        :header="'Credentials'"
        :content="[
          {field: 'Client ID', value: [user.client_id]},
          {field: 'Client Secret', value: [user.client_secret]},
        ]"
      />
      <button @click="generateSecret" type="submit">
          Generate Secret
      </button>
    </app-content>
  </div>
</template>

<script>
import SectionBox from '@/components/AnalysisView/SectionBox.vue';

import {authStore} from '../stores/authStore';

import Header from '../components/Header.vue';

export default {
  name: 'account-view-component',
  components: {
    Header,
    SectionBox,
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
