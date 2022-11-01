<template>
    <app-content>
        <img src="@/assets/rosalution-logo.svg" class="rosalution-logo-large" />
        <h2>
            You have been successfully logged out of Rosalution.
        </h2>
        <p>
          <router-link :to="{name: 'login'}">
            <button class="rosalution-button login-uab-button">
                Return
            </button>
          </router-link>
        </p>
    </app-content>
</template>

<script>
import {authStore} from '@/stores/authStore.js';

export default {
  data: function() {
    return {
      store: authStore,
    };
  },
  async created() {
    const token = this.store.getToken();
    if (token) {
      const response = await this.store.logout();
      if (response && 'url' in response) {
        this.redirectUrl(response['url']);
      }
    }
  },
  methods: {
    redirectUrl(url) {
      window.location.href = url;
    },
  },
};

</script>

<style scoped>

 app-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-top: 10rem;
}

.rosalution-logo-large {
  width: 8.25rem;
  height: 6.563rem;
  margin-top: 0.938rem;
}

</style>
