<template>
  <div>
    <app-header>
      <RosalutionHeader
        :username="user.username"
        @logout="this.onLogout"
        data-test="rosalution-header"
      >
      <span class="empty-fill"></span>
      </RosalutionHeader>
    </app-header>
    <app-content>
      <SectionBox
        ref="user-section-box"
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
          {field: 'Client ID', value: [user.clientId]},
          {
            field: 'Client Secret',
            value: [user.clientSecret ? '<span class=\"click-to-reveal\">click to reveal</span>' : '<empty>'],
            clickToReveal: user.clientSecret ? true : false,
          },
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

import RosalutionHeader from '../components/RosalutionHeader.vue';

export default {
  name: 'account-view-component',
  components: {
    RosalutionHeader,
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
    async onLogout() {
      this.$router.push({path: '/rosalution/logout'});
    },
    reveal(index) {
      this.content[index].clickToReveal = false;
      this.content[index].value[0] = this.content[index].clickToRevealValue;
    },
  },
};
</script>

<style>
.click-to-reveal {
  cursor: pointer;
  text-decoration: underline;
}
.empty-fill {
  flex: 1 1 auto;
  display: inline-flex;
}
</style>
