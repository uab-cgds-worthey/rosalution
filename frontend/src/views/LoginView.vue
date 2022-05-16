<template>
    <div class="center">
        <h1 v-if="username != ''">Welcome, {{ this.username }}</h1>
        <h1 v-else>Authentication</h1>
          <button @click="login" type="submit">Login</button>
          <br />
          <br />
          <button @click="logout" type="submit">Logout</button>
    </div>
</template>

<script>

export default {
  data() {
    return {
      username: '',
    };
  },
  methods: {
    async login() {
      const loginUrl = '/divergen/api/auth/login';
      const newURL = await fetch(loginUrl, {
        method: 'GET',
        mode: 'cors',
      });

      const response = await newURL.json();

      if ('url' in response) {
        console.log(response['url']);
        window.location = response['url'];
      } else if ('username' in response) {
        console.log(response['username']);
        this.username = response['username'];
      }
    },
    async logout() {
      const logoutUrl = '/divergen/api/auth/logout';
      const newURL = await fetch(logoutUrl, {
        method: 'GET',
        mode: 'cors',
      });

      const response = await newURL.json();
      console.log(response['url']);

      window.location = response['url'];
    },
  },
};
</script>

<style>
.center {
  margin: auto;
  text-align: center;
  width: 50%;
  border: 3px solid green;
  padding: 10px;
}
</style>
