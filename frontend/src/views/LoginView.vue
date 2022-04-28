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
      const loginUrl = '/divergen/api/login';
      console.log(loginUrl);
      await fetch(loginUrl, {
        method: 'GET',
        mode: 'no-cors',
        cache: 'no-cache',
      });
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
