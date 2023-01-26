<template>
  <div>
      User Information
      <p></p>
      <button @click="generateSecret" type="submit">
          Generate Secret
      </button>
  </div>
</template>

<script>
import {authStore} from '../stores/authStore';

export default {
  methods: {
    async generateSecret() {
      const userObject = await authStore.generateSecret();
      console.log(userObject);
    },
  },
};
</script>