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
      <UserInfoBox
        :header="'User'"
        :username="user.username"
        :fullName="user.full_name"
        :email="user.email"/>
      <CredentialsBox
        :header="'Credentials'"
        :clientId="user.clientId"
        :clientSecret="secretValue"
        data-test="credentials"
        :key="showSecretValue"
        @display-secret= this.onToggleSecret
        @generate-secret = this.onGenerateSecret
        :secretExists="clientSecretExists"
        />
    </app-content>
  </div>
</template>

<script>
import UserInfoBox from '@/components/AccountView/UserInfoBox.vue';
import CredentialsBox from '@/components/AccountView/CredentialsBox.vue';

import {authStore} from '../stores/authStore';

import RosalutionHeader from '../components/RosalutionHeader.vue';

export default {
  name: 'account-view-component',
  components: {
    RosalutionHeader,
    UserInfoBox,
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
    secretValue() {
      if (this.showSecretValue) {
        return this.clientSecret;
      }
      if (this.clientSecret) {
        return '<click to show>';
      }

      return '<empty>';
    },
    clientSecretExists() {
      return Boolean(this.clientSecret);
    },
  },
  methods: {
    async onGenerateSecret() {
      await authStore.generateSecret();
      const updatedUser = await authStore.getAPICredentials();
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
