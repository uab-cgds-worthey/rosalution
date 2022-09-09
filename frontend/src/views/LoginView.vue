<template>
    <app-content>
      <img src="@/assets/rosalution-logo.svg" class="rosalution-logo-large" img>
      <h2>
        Rosalution
      </h2>
      <span style="font-weight: 600; font-size: 1rem;">Local Development Login</span>
      <input class="username-input" v-model="username" placeholder="username" data-test="username-input"/>
      <button class="login-local-button" @click="developmentLogin" type="submit" data-test="local-login-button">
        Login
      </button>
      <hr class="login-divider">
      <button class="login-uab-button" @click="productionLogin" type="submit" data-test="prod-login-button">
        UAB LOGIN
      </button>
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
  created() {
    label:
    document.querySelector('#app').appendChild(document.createTextNode("AAAAAWWWWEEEEESSSSSOOOOOMMMMMEEEEE"));
    
  },
  methods: {
    async developmentLogin() {
      // Password is hard coded. Taking it out would require a rewrite of the backend as of now.
      if (this.username != '') {
        const userData = {'username': this.username, 'password': 'secret'};
        await Auth.loginOAuth(userData);
      }
    },
    async productionLogin() {
      await Auth.loginCas();
    },
  },
};
</script>

<style scoped>

app-content{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 60%;
}

h2 {
  font-weight: bold;
  font-size: 1.875rem;
  margin-top: 0.625rem;
}

.rosalution-logo-large {
  width: 8.25rem;
  height: 6.563rem;
  margin-top: 0.938rem;
}

.username-input {
  text-align: center;
  font-size: 0.813rem;
  margin-top: 1.563rem;
  border: solid;
  border-radius: 0.438rem;
  border-color: var(--rosalution-grey-100);
  width: 9.375rem;
  height: 1.688rem;
}

.username-input::placeholder {
  color: var(--rosalution-grey-300);
}

.login-local-button {
  background-color: var(--rosalution-purple-100);
  color: var(--rosalution-purple-300);
  font-family: "Proxima Nova", sans-serif;
  font-weight: 700;
  font-size: 1.125rem;
  height: 1.75rem;
  width: 7rem;
  border: none;
  border-radius: 1.563rem;
  margin-top: 1.25rem;
}

.login-local-button:hover {
  background-color: var(--rosalution-purple-200);
}

hr.login-divider {
  margin-top: 1.25rem;
  border: none;
  width: 23.75rem;
  height: 0.063rem;
  background-color: var(--rosalution-grey-200);
}

.login-uab-button {
  background-color: var(--rosalution-purple-100);
  color: var(--rosalution-purple-300);
  font-family: "Proxima Nova", sans-serif;
  font-weight: 700;
  font-size: 1.125rem;
  height: 2.25rem;
  width: 12rem;
  border: none;
  border-radius: 1.563rem;
  margin-top: 0.625rem;
}

.login-uab-button:hover {
  background-color: var(--rosalution-purple-200);
}

</style>
