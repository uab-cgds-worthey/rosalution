import Requests from '@/requests.js';

export default {
  /* CAS Login Functions */

  async loginCas() {
    const baseUrl = '/divergen/api/';
    const urlQuery = 'auth/login';
    const body = await Requests.get(baseUrl + urlQuery);
    if ('errors' in body) {
      const errorString = body.data.errors.map((error) => error.message).join('; ');
      throw new Error('Failed to login: ' + errorString);
    }

    return body;
  },
  async logoutCas() {
    const baseUrl = '/divergen/api/';
    const urlQuery = 'auth/logoutCas';
    const body = await Requests.get(baseUrl + urlQuery);
    if ('errors' in body) {
      const errorString = body.data.errors.map((error) => error.message).join('; ');
      throw new Error('Failed to login: ' + errorString);
    }

    return body;
  },

  /* OAuth2 Login Functions */

  async login(data) {
    const baseUrl = '/divergen/api/';
    const urlQuery = 'auth/token';
    const body = await Requests.postLogin(baseUrl + urlQuery, data);
    if ('errors' in body) {
      const errorString = body.data.errors.map((error) => error.message).join('; ');
      throw new Error('Failed to login: ' + errorString);
    }

    return body;
  },
  async verifyUser() {
    const baseUrl = '/divergen/api/';
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
    const baseUrl = '/divergen/api/';
    const urlQuery = 'auth/logout';

    const body = await Requests.get(baseUrl + urlQuery);
    if ('errors' in body) {
      const errorString = body.data.errors.map((error) => error.message).join('; ');
      throw new Error('Failed to logout: ' + errorString);
    }

    return body;
  },
};
