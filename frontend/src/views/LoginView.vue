<template>
    <div class="center">
        <h1>{{ this.message }}</h1>
        <h2 v-if="error != ''" style="color: red">unauthorized</h2>
          <input v-model="username" placeholder="username"/>
          <br />
          <br />
          <input v-model="password" placeholder="password" type="password"/>
          <br />
          <br />
          <button @click="loginOAuth" type="submit">Login</button>
          <br />
          <br />
          <button @click="verifyUser" type="submit">Verify User</button>
          <br />
          <br />
          <button @click="logoutOAuth" type="submit">Logout</button>
          <br />
          <br />
          <br />
          <button @click="loginCAS" type="submit">Login BlazerID</button>
          <br />
          <br />
          <button @click="logoutCAS" type="submit">Logout BlazerID</button>
          <br />
          <br />
          <router-link :to="{ path: '/rosalution' }">
            <button @click="back" type="submit">Back</button>
          </router-link>
    </div>
</template>

<script>
import Auth from '../models/authentication';

export default {
  data() {
    return {
      message: 'Authenticate User',
      error: '',
      username: '',
      password: '',
    };
  },
  methods: {
    /* CAS Login Functions */
    async loginCAS() {
      const response = await Auth.loginCas();

      if ('url' in response) {
        window.location = response['url'];
      } else if ('username' in response) {
        this.username = response['username'];
      }
    },
    async logoutCAS() {
      const response = await Auth.logoutCas();

      window.location = response['url'];
    },

    /* OAuth2 Login Functions */

    async loginOAuth() {
      const userData = {'username': this.username, 'password': this.password};

      const responseJson = await Auth.login(userData);
      console.log(responseJson);

      this.error = '';
    },
    // TODO: Remove this function and migrate it to the ./models/users.js file
    async verifyUser() {
      const user = await Auth.verifyUser();

      // TODO: Handle Unauthorized error
      // Right now this is how we're handling unauthorization errors
      // There needs to be a proper way to user09e these errors, otherwise each function will
      // have their own error message
      if (user.error) {
        this.error = user.error;
        return;
      }

      this.message = 'Welcome, ' + user.username;
    },

    async logoutOAuth() {
      const response = await Auth.logout();
      console.log(response);
      this.message = 'Logged out successfully!';
      this.username = '';
      this.password = '';
      this.error = '';
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
