<template>
    <div class="center">
        <h1 v-if="username != ''">Welcome, {{ this.username }}</h1>
        <h1 v-else>Authentication</h1>
          <button @click="login" type="submit">Login</button>
          <br />
          <br />
          <button @click="validate" type="submit">Validate</button>
          <br />
          <br />
          <button @click="test" type="submit">Test</button>
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
      const loginUrl = '/divergen/api/login';
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
    async validate() {
      const validateUrl = '/divergen/api/validate';
      const newURL = await fetch(validateUrl, {
        method: 'GET',
        mode: 'cors',
      });

      const response = await newURL.json();

      this.username = response['username'];
      console.log(this.username);
    },
    async test() {
      const validateUrl = '/divergen/api/test';
      const newURL = await fetch(validateUrl, {
        method: 'GET',
        mode: 'cors',
      });

      const response = await newURL.json();

      console.log(response);
    },
    async logout() {
      const logoutUrl = '/divergen/api/logout';
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
