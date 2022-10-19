import {describe, it, expect, beforeEach, afterEach} from 'vitest';

import Requests from '@/requests.js';

import {authStore} from '@/stores/authStore.js';
import sinon from 'sinon';

describe('user.js', () => {
  const sandbox = sinon.createSandbox();
  let mockGetRequest;
  let mockPostLoginRequest;

  beforeEach(() => {
    mockGetRequest = sandbox.stub(Requests, 'get');
    mockPostLoginRequest = sandbox.stub(Requests, 'postLogin');
  });

  afterEach(() => {
    sandbox.restore();
  });

  it('Initiates a development login and recieves a bearer token', async () => {
    mockPostLoginRequest.returns(userResponse);

    const userData = {'username': 'fakeUser', 'password': ''};
    await authStore.loginDevelopment(userData);
  });

  it('Queries the user from the backend session, user is NOT logged in', async () => {
    mockGetRequest.returns({'username': ''});
    const username = await authStore.verifyToken();
    expect(username['username']).to.equal('');
  });

  it('Queries the user from the backend session, user is logged in', async () => {
    mockGetRequest.returns({'username': 'UABProvider'});
    const username = await authStore.verifyToken();
    expect(username['username']).to.equal('UABProvider');
  });
});

const userResponse = {
  'username': 'fakename',
  'full_name': 'Fake Name',
  'email': 'fakemail@fake.com',
};
