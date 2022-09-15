<template>
    <app-content>
      <img src="@/assets/rosalution-logo.svg" class="rosalution-logo-large" img>
      <h2>
        Rosalution
      </h2>
      <button
        class="rosalution-button login-uab-button"
        @click="productionLogin"
        type="submit"
        data-test="prod-login-button"
      >
        UAB LOGIN
      </button>
    </app-content>
</template>

<script>
import Auth from '../models/authentication.js';

export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  mounted() {
    /*
    This mounted function is used to turn on and off the development login components. They are unused in the production
    deployment of Rosalution, but are necessary here as we can strip all the components at the time of build with rollup
    and it won't appear in the final product.
    */


    development: { // eslint-disable-line no-unused-labels
      const that = this;

      /* Development Login Label */
      const localDevelopmentString = document.createElement('span');
      localDevelopmentString.setAttribute('style', 'font-weight: 600; font-size: 1rem;');
      localDevelopmentString.innerText = 'Local Development Login';

      /* Development Username Input */
      const localUsernameInput = document.createElement('input');
      localUsernameInput.classList.add('rosalution-input');
      localUsernameInput.setAttribute('placeholder', 'Username');
      localUsernameInput.setAttribute('id', 'username-input-id');
      localUsernameInput.setAttribute('data-test', 'username-input');
      localUsernameInput.addEventListener('input', function(text) {
        const inputText = document.getElementById('username-input-id').value;
        that.username = inputText;
      });

      /* Development Login Button */
      const localLoginButton = document.createElement('button');
      localLoginButton.classList.add('rosalution-button');
      localLoginButton.setAttribute('style', 'margin-top: 0.625rem;');
      localLoginButton.setAttribute('data-test', 'local-login-button');
      localLoginButton.addEventListener('click', this.developmentLogin);
      localLoginButton.innerText = 'Login';

      /* The divider line between local and UAB login */
      const loginDivider = document.createElement('hr');
      loginDivider.setAttribute('style',
          `margin-top: 1.25rem;
        border: none;
        width: 23.75rem;
        height: 0.063rem;
        background-color: var(--rosalution-grey-200);
      `);

      const localLoginPage = document.querySelector('button');

      const parentDiv = localLoginPage.parentNode;
      parentDiv.insertBefore(localDevelopmentString, localLoginPage);
      parentDiv.insertBefore(localUsernameInput, localLoginPage);
      parentDiv.insertBefore(localLoginButton, localLoginPage);
      parentDiv.insertBefore(loginDivider, localLoginPage);
    }
  },
  methods: {
    async developmentLogin() {
      // Password is hard coded. Taking it out would require a rewrite of the backend as of now.
      console.log('I am a thing being called');
      console.log(this.username);
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

.login-uab-button {
  height: 2.25rem;
  width: 12rem;
  margin-top: 0.625rem;
}

.login-uab-button:hover {
  background-color: var(--rosalution-purple-200);
}

</style>
