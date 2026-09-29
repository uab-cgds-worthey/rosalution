import {computed} from 'vue';
import {useRouter} from 'vue-router';

import {authStore} from '@/stores/authStore.js';


export function useAuth() {
  console.log("REAL: useAuth Method Being Called");
  const router = useRouter();

  const username = computed(() => {
    return authStore.getUsername();
  });

  const hasWritePermissions = computed(() => {
    return authStore.hasWritePermissions();
  });

  async function logout() {
    router.push({name: 'logout'});
  }

  return {
    username,
    hasWritePermissions,
    logout,
  };
};
