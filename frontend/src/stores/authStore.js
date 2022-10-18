import Requests from '@/requests.js';

const authStore = {
  state: {
    full_name: '',
    username: '',
    email: '',
    roles: [],
  },
  async saveState(user) {
    this.state.full_name = user['full_name'];
    this.state.username = user['username'];
    this.state.email = user['email'];
  },
  getToken() {
    if (document.cookie == '') {
      return null;
    }

    const rosalutionCookie = document.cookie.split(';').find((row) => row.startsWith('rosalution_TOKEN='));

    if (typeof(rosalutionCookie) == 'undefined') {
      return null;
    }

    return rosalutionCookie.split('=')[1];
  },
  hasRole(role) {
    return this.state.roles.includes(role);
  },
  /* CAS Login Functions */
  async loginCas() {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'auth/login';
    const body = await Requests.get(baseUrl + urlQuery);
    if ('errors' in body) {
      const errorString = body.data.errors.map((error) => error.message).join('; ');
      throw new Error('Failed to login: ' + errorString);
    }

    return body;
  },
  async logoutCas() {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'auth/logoutCas';
    const body = await Requests.get(baseUrl + urlQuery);
    if ('errors' in body) {
      const errorString = body.data.errors.map((error) => error.message).join('; ');
      throw new Error('Failed to login: ' + errorString);
    }

    return body;
  },
  /* OAuth2 Login Functions */
  async loginOAuth(data) {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'auth/token';
    const body = await Requests.postLogin(baseUrl + urlQuery, data);
    if ('errors' in body) {
      const errorString = body.data.errors.map((error) => error.message).join('; ');
      throw new Error('Failed to login: ' + errorString);
    }

    this.saveState(body);
  },
  async verifyUser() {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'auth/verify';

    const body = await Requests.get(baseUrl + urlQuery);
    if ('errors' in body) {
      const errorString = body.data.errors.map((error) => error.message).join('; ');
      console.log(errorString);
      throw new Error('Failed to verify user: ' + errorString);
    }

    return body;
  },
  async logout() {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'auth/logout';

    const body = await Requests.get(baseUrl + urlQuery);
    if ('errors' in body) {
      const errorString = body.data.errors.map((error) => error.message).join('; ');
      throw new Error('Failed to logout: ' + errorString);
    }

    return body;
  },
  /* User specific endpoints */
  async fetchUser() {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'auth/get_user';

    const body = await Requests.get(baseUrl + urlQuery);

    if ('errors' in body) {
      const errorString = body.data.errors.map((error) => error.message).join('; ');
      throw new Error('Failed to fetch user: ' + errorString);
    }

    return body;
  },
};

export {authStore};
