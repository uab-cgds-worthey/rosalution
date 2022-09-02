<template>
    <app-content>
      <div class="center">
        <img src="@/assets/rosalution-logo.svg" class="rosalution-logo-large" img>
        <span style="font-weight: bold; font-size: 30px; margin-top: 10px;">Rosalution</span>
        <span class= "" style="font-weight: 600; font-size: 15px; margin-top: 10px;">Local Development Login</span>
        <input class="username-input" v-model="username" placeholder="username"/>
        <button class="login-local-button" @click="loginOAuth" type="submit">Login</button>
        <!-- <hr width="75%" color="#C4C4C4" size="1"> -->
        <hr>
        <button class="login-uab-button" @click="loginCAS" type="submit">UAB LOGIN</button>
      </div>
    </app-content>
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
      const userData = {'username': this.username, 'password': 'secret'};

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
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 60%;
}

.rosalution-logo-large {
  width: 132px;
  height: 105px;
  margin-top: 15px;
}

.username-input {
  text-align: center;
  font-size: 13px;
  margin-top: 25px;
  border: solid;
  border-radius: 7px;
  border-color: var(--rosalution-grey-100);
  width: 150px;
  height: 27px;
}

.username-input::placeholder {
  color: var(--rosalution-grey-300);
}

.login-local-button {
  background-color: var(--rosalution-purple-100);
  color: var(--rosalution-purple-300);
  font-family: "Proxima Nova", sans-serif;
  font-weight: 700;
  font-size: 18px;
  height: 1.75rem;
  width: 7rem;
  border: none;
  border-radius: 25px;
  margin-top: 20px;
}

.login-local-button:hover {
  background-color: var(--rosalution-purple-200);
}

hr {
  margin-top: 20px;
  border: none;
  width: 380px;
  height: 1px;
  background-color: var(--rosalution-grey-200);
}

.login-uab-button {
  background-color: var(--rosalution-purple-100);
  color: var(--rosalution-purple-300);
  font-family: "Proxima Nova", sans-serif;
  font-weight: 700;
  font-size: 18px;
  height: 2.25rem;
  width: 12rem;
  border: none;
  border-radius: 25px;
  margin-top: 10px; 
}

.login-uab-button:hover {
  background-color: var(--rosalution-purple-200);
}

</style>
