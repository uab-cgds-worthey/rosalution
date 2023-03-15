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
        :clientId="user.clientId"
        :clientSecret="secretValue"
        data-test="credentials"
        :key="showSecretValue"
        @display-secret= this.onToggleSecret
        @generateSecret = this.onGenerateSecret
        :onSecretGenerated="updateSecretValue"
        />
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
      clientSecret: '',
    };
  },
  created() {
    this.clientSecret = this.user.clientSecret;
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
        return this.clientSecret;
      }
      if (this.clientSecret) {
        return '<click to show>';
      }

      return '<empty>';
    },
  },
  methods: {
    async onGenerateSecret() {
      await authStore.generateSecret();
      const updatedUser = await authStore.getAPICredentials();
      console.log(updatedUser);
      console.log(updatedUser.client_secret);
      this.clientSecret = updatedUser.client_secret;
    },
    async onLogout() {
      this.$router.push({path: '/rosalution/logout'});
    },
    async onToggleSecret() {
      if (!this.showSecretValue && this.secretValue !== '<empty>') {
        this.showSecretValue = !this.showSecretValue;
      }
    },
    updateSecretValue() {
      this.showSecretValue = true;
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
