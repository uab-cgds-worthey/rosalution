import Requests from '@/requests.js';

export default {
    async login() {
        const baseUrl = '/divergen/api/';
        const urlQuery = 'auth/token';
        const body = await Requests.get(baseUrl + urlQuery);
        if ('errors' in body) {
            const errorString = body.data.errors.map((error) => error.message).join('; ');
            throw new Error('Failed to fetch analyses: ' + errorString);
        }

        return body;
    },
    async logout() {
        const baseUrl = '/divergen/api';
        const urlQuery = 'auth/logout';
    }
};
