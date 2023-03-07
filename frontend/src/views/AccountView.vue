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
        data-test="credentials"
        :key="showSecretValue"
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
    return {
      showSecretValue: false,
    };
  },
  computed: {
    user() {
      return authStore.getUser();
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
      const userObject = await authStore.generateSecret();
      console.log(userObject);
    },
    async onLogout() {
      this.$router.push({path: '/rosalution/logout'});
    },
    toggleSecret() {
      if (!this.showSecretValue && this.secretValue[0] !== '<empty>') {
        this.showSecretValue = !this.showSecretValue;
      }
    },
  },
};
</script>
