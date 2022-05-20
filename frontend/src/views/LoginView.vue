<template>
    <div class="center">
        <h1 v-if="username != ''">Welcome, {{ this.username }}</h1>
        <h1 v-else>Authentication</h1>
          <input v-model="username" placeholder="username"/>
          <br />
          <br />
          <input v-model="password" placeholder="password" type="password"/>
          <br />
          <br />
          <button @click="loginTemp" type="submit">Login</button>
          <br />
          <br />
          <button @click="verify" type="submit">Verify</button>   
          <br />
          <br />
          <button @click="testInject" type="submit">Test</button>   
          <br />
          <br />
          <button @click="logout" type="submit">Logout</button>
          <br />
          <br />
          <br />
          <br />
          <router-link :to="{ path: '/divergen' }">
            <button @click="back" type="submit">Back</button>
          </router-link>
    </div>
</template>

<script>
import { userStore } from '../authStore.js'
import { cookie } from '../cookie.js'

export default {
  data() {
    return {
      username: '',
      password: '',
      userStore
    };
  },
  // inject: ['userStore'],
  methods: {
    async loginTemp() {      
      const response = await fetch("http://local.divergen.cgds/divergen/api/auth/token", {
          method: 'POST',
          headers: {
              "accept": "application/json",
              "Content-Type": "application/x-www-form-urlencoded",
          },
          mode: 'cors',
          cache: 'no-cache',
          body: 'grant_type=password&scope=read+write&username=' + this.username + '&password=' + this.password,
      });

      const responseJson = await response.json();

      console.log(responseJson);

      userStore.saveState(responseJson);
      cookie.setCookie(responseJson['access_token']);

      // this.userStore.state.token = responseJson;
    },
    async verify() {
      const verifyURL = '/divergen/api/auth/verify';
      const newURL = await fetch(verifyURL, {
        method: 'GET',
        mode: 'cors',
      });

      const response = await newURL.json();

      console.log(response);
    },
    async testInject() {
      console.log(userStore.state.token);
    },
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