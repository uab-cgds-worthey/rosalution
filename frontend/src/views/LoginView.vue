<template>
    <div class="center">
        <h1>Authentication</h1>
        <form @submit.prevent="login">
            <button type="submit">Login</button>
            <br />
            <br />
            <br />
            <button type="submit">Logout</button>
        </form>
    </div>
</template>

<script>

export default {
  methods: {
    async login() {
      const loginUrl = '/divergen/api/logintest';
      const newURL = await fetch(loginUrl, {
      method: 'GET',
      mode: 'cors',
    });

      const response = await newURL.json()
      console.log(response['url']);
      console.log()
      window.location = response['url'];
    },
    async logout() {

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
