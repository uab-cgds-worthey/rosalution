import Requests from '@/requests.js';

export default {
  async getUser() {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'auth/get_user';

    const body = await Requests.get(baseUrl + urlQuery);

    if ('errors' in body) {
      const errorString = body.data.errors.map((error) => error.message).join('; ');
      throw new Error('Failed to fetch user: ' + errorString);
    }

    return body;
  },
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
};
