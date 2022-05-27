import Requests from '@/requests.js';

export default {
  async getUser() {
    const baseUrl = '/divergen/api/';
    const urlQuery = 'auth/get_user';

    const body = await Requests.get(baseUrl + urlQuery);

    if ('errors' in body) {
      const errorString = body.data.errors.map((error) => error.message).join('; ');
      throw new Error('Failed to fetch user: ' + errorString);
    }

    return body;
  },
};
