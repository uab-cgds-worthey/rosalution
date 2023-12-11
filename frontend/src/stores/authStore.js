import Requests from '@/requests.js';

const authStore = {
  state: {
    full_name: '',
    username: '',
    email: '',
    roles: [],
    clientId: '',
    clientSecret: '',
  },
  clearState() {
    this.state.full_name = '';
    this.state.username = '';
    this.state.email = '';
    this.state.roles = [];

    this.state.clientId = '';
    this.state.clientSecret = '';
  },
  saveState(user) {
    this.state.full_name = user['full_name'];
    this.state.username = user['username'];
    this.state.email = user['email'];
    this.state.roles.push(user['scope']);
    this.state.clientId = user['client_id'];
    
    user['client_secret'] ? this.state.clientSecret = user['client_secret'] : '';
  },
  getUser() {
    return {...this.state};
  },
  getUsername() {
    return this.state.username;
  },
  getClientId() {
    return this.state.clientId;
  },
  hasWritePermissions() {
    return this.hasRole('write');
  },
  getToken() {
    if (document.cookie == '') {
      return null;
    }

    const rosalutionCookie = document.cookie.split('; ').find((row) => row.startsWith('rosalution_TOKEN='));

    if (typeof(rosalutionCookie) == 'undefined') {
      return null;
    }

    return rosalutionCookie.split('=')[1];
  },
  hasRole(role) {
    return this.state.roles.includes(role);
  },
  async loginUAB() {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'auth/login';
    const body = await Requests.get(baseUrl + urlQuery);

    return body;
  },
  async loginDevelopment(data) {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'dev/loginDev';
    const body = await Requests.postLogin(baseUrl + urlQuery, data);

    return body;
  },
  async verifyToken() {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'auth/verify_token';

    const body = await Requests.get(baseUrl + urlQuery);

    return body;
  },
  async getAPICredentials() {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'auth/get_user_credentials';

    const body = await Requests.get(baseUrl + urlQuery);

    return body;
  },
  async generateSecret() {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'auth/generate_secret';

    const body = await Requests.get(baseUrl + urlQuery);

    return body;
  },
  async logout() {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'auth/logout';

    const body = await Requests.get(baseUrl + urlQuery);

    return body;
  },
};

export {authStore};
