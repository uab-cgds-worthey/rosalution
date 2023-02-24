<template>
  <div>
    <app-header>
      <RosalutionHeader
        :username="user.username"
        @logout="this.onLogout"
        data-test="rosalution-header">
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
      <SectionBox
        :header="'Credentials'"
        :content="[
          { field: 'Client ID', value: [user.clientId] },
          {
            field: 'Client Secret',
            value: secretValue,
          },
        ]"
        @click="toggleSecret"
        ref="credentials"
        :key="showSecret"
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

import RosalutionHeader from '../components/RosalutionHeader.vue';

export default {
  name: 'account-view-component',
  components: {
    RosalutionHeader,
    SectionBox,
  },
  data() {
    const user = authStore.getUser();
    return {
      showSecret: false,
      secretValue: user.clientSecret ? ['<click to show>'] : ['<empty>'],
    };
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
    async onLogout() {
      this.$router.push({path: '/rosalution/logout'});
    },
    toggleSecret() {
      if (!this.showSecret && this.secretValue[0] !== '<empty>') {
        this.showSecret = !this.showSecret;
        this.updateSecretValue();
      }
    },
    updateSecretValue() {
      if (this.showSecret) {
        this.secretValue = [this.user.clientSecret];
      } else {
        this.secretValue = ['<click to show>'];
      }
    },
  },
};
</script>
