<template>
    <div class="center">
        <h1>Authentication</h1>
          <button @click="login" type="submit">Login</button>
          <br />
          <br />
          <button @click="validate" type="submit">Validate</button>
          <br />
          <br />
          <button @click="logout" type="submit">Logout</button>
    </div>
</template>

<script>

export default {
  methods: {
    async login() {
      const loginUrl = '/divergen/api/login';
      const newURL = await fetch(loginUrl, {
        method: 'GET',
        mode: 'cors',
      });

      const response = await newURL.json();
      console.log(response['url']);

      window.location = response['url'];
    },
    async validate() {
      console.log('Validating the login');
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
