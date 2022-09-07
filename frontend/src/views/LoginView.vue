<template>
    <app-content>
      <div class="center">
        <img src="@/assets/rosalution-logo.svg" class="rosalution-logo-large" img>
        <span style="font-weight: bold; font-size: 30px; margin-top: 10px;">Rosalution</span>
        <span class= "" style="font-weight: 600; font-size: 15px; margin-top: 10px;">Local Development Login</span>
        <input class="username-input" v-model="username" placeholder="username"/>
        <button class="login-local-button" @click="developmentLogin" type="submit">Login</button>
        <hr class="login-divider">
        <button class="login-uab-button" @click="productionLogin" type="submit">UAB LOGIN</button>
      </div>
    </app-content>
</template>

<script>
import Auth from '../models/authentication.js';

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
    async developmentLogin() {
      // Password is hard coded. Taking it out would require a rewrite of the backend as of now.
      const userData = {'username': this.username, 'password': 'secret'};
      Auth.loginOAuth(userData);
    },
    async productionLogin() {
      Auth.loginCas();
    }
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

hr.login-divider {
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
