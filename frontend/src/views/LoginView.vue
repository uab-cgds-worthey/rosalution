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
import {authStore} from '../stores/authStore';

export default {
  data() {
    return {
      store: authStore,
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
      if (this.username != '') {
        const userData = {'username': this.username, 'password': 'secret'};
        await this.store.loginOAuth(userData);
        this.$router.push('/rosalution/');
      }
    },
    async productionLogin() {
      const response = await this.store.loginCas();

      /*
      The CAS login sends a URL as a response. The URL can change depending on whether or not you have a valid
      login token. If you are not logged in, it will send you to the UAB blazerid page. If you are logged in, it
      will send you to the Analysis Listing page.
      */
      if (response && 'url' in response) {
        window.location = response['url'];
      }
    },
  },
};
</script>

<style scoped>

app-content{
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  margin-top: 10rem;
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
