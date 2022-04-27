<template>
    <div class="center">
        <h1>Login</h1>
        <form @submit.prevent="login">
            <input v-model="username" placeholder="username" />
            <br />
            <br />
            <input v-model="password" placeholder="password" type="password" />
            <br />
            <br />
            <button type="submit">Login</button>
        </form>
    </div>
</template>

<script>

export default {
  data: () => {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async login() {

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
