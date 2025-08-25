<template>
  <app-header>
    <RosalutionHeader
      :username="user.username"
      @logout="onLogout"
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
      @display-secret= onToggleSecret
      @generate-secret = onGenerateSecret
      :secretExists="clientSecretExists"
      />
  </app-content>
  <app-footer>
    <RosalutionFooter></RosalutionFooter>
  </app-footer>
</template>

<script setup>
import {onBeforeMount, ref, computed} from 'vue';
import {useRouter} from 'vue-router';

import CredentialsBox from '@/components/AccountView/CredentialsBox.vue';
import RosalutionFooter from '@/components/RosalutionFooter.vue';
import RosalutionHeader from '@/components/RosalutionHeader.vue';
import UserInfoBox from '@/components/AccountView/UserInfoBox.vue';

import {authStore} from '@/stores/authStore';

const router = useRouter();

const showSecretValue = ref(false);
const clientSecret = ref('');

const user = computed(() => {
  return authStore.getUser();
});

const secretValue = computed(() => {
  if (showSecretValue.value) {
    return clientSecret.value;
  }

  if (clientSecret.value) {
    return '<click to show>';
  }

  return '<empty>';
});

const clientSecretExists =  computed(() => {
  return Boolean(clientSecret.value);
});

onBeforeMount(() => {
  clientSecret.value = user.value.clientSecret;
});

async function onGenerateSecret() {
  await authStore.generateSecret();
  const updatedUser = await authStore.getAPICredentials();
  clientSecret.value = updatedUser.client_secret;
}

async function onLogout() {
  router.push({name: 'logout'});
}

async function onToggleSecret() {
  if (!showSecretValue.value && secretValue.value !== '<empty>') {
    showSecretValue.value = true;
  }
}

document.title = 'Account | rosalution';
</script>

<style>
app-content {
  display: flex;
  flex-direction: column;
  gap: var(--p-10);
}

.empty-fill {
  flex: 1 1 auto;
  display: inline-flex;
}
</style>
