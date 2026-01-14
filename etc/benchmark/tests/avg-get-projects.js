import http from 'k6/http';
import secrets from 'k6/secrets';
import { sleep, check } from 'k6';

import { rosalutionAuth } from '../config/auth.js';

const BASE_URL = __ENV.BASE_URL || 'http://backend:8000'

export const options = {
  vus: 10,
  duration: '30s',
  thresholds: {
    http_req_failed: ['rate<0.01'], // http errors should be less than 1%
    http_req_duration: ['p(95)<200'] // 95% of requests should be below 200ms
  }
};

export async function setup() {
  const clientId = await secrets.get('CLIENT_ID')
  const clientSecret = await secrets.get('CLIENT_SECRET')

  const authToken = rosalutionAuth(BASE_URL, clientId, clientSecret)

  return {
    auth_token: authToken
  }
}

export default async function(data) {
  const authHeader = {
    headers: {
      'Authorization': `Bearer ${data.auth_token}`
    }
  };
  
  let res = http.get(`${BASE_URL}/analysis/summary?profile=1&profile_type=html`, authHeader);

  check(res, { "status is 200": (res) => res.status === 200 });
  sleep(1);
}

