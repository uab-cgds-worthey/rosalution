<template>
  <div>
    <app-header>
      <RosalutionHeader
        :username="user.username"
        @logout="this.onLogout"
        data-test="rosalution-header">
        <span class="empty-fill"></span>
      </RosalutionHeader>
    </app-header>
    <app-content>
      <SectionBox
        :header="'User'"
        :content="[
          { field: 'Username', value: [user.username] },
          { field: 'Full Name', value: [user.full_name] },
          { field: 'Email', value: [user.email] },
        ]" />
      <CredentialsBox
        :header="'Credentials'"
        :content= credentialsContent
        data-test="credentials"
        :key="showSecretValue"
        @toggle= this.ontoggleSecret
        />
      <button @click="generateSecret" type="submit">
        Generate Secret
      </button>
    </app-content>
  </div>
</template>

<script>
import SectionBox from '@/components/AnalysisView/SectionBox.vue';
import CredentialsBox from '@/components/AccountView/CredentialsBox.vue';

import {authStore} from '../stores/authStore';

import RosalutionHeader from '../components/RosalutionHeader.vue';

export default {
  name: 'account-view-component',
  components: {
    RosalutionHeader,
    SectionBox,
    CredentialsBox,
  },
  data() {
    return {
      showSecretValue: false,
    };
  },
  computed: {
    user() {
      return authStore.getUser();
    },
    credentialsContent() {
      const content = [
        {field: 'Client ID', value: [this.user.clientId]},
        {
          field: 'Client Secret',
          value: this.secretValue,
          clickable: true,
        },
      ];
      return content;
    },
    secretValue() {
      if (this.showSecretValue) {
        return [this.user.clientSecret];
      }
      if (this.user.clientSecret) {
        return ['<click to show>'];
      }

      return ['<empty>'];
    },
  },
  methods: {
    async generateSecret() {
      await authStore.generateSecret();
    },
    async onLogout() {
      this.$router.push({path: '/rosalution/logout'});
    },
    async ontoggleSecret() {
      if (!this.showSecretValue && this.secretValue[0] !== '<empty>') {
        this.showSecretValue = !this.showSecretValue;
      }
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
