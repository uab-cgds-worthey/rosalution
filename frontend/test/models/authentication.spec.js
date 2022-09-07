import {describe, it, expect, beforeEach, afterEach} from 'vitest';

import Auth from '@/models/authentication.js';
import Requests from '@/requests.js';
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
    mockPostLoginRequest.returns(test_token);

    const userData = {'username': 'fakeUser', 'password': 'secret'};
    const token = await Auth.loginOAuth(userData)
    expect(token.access_token).to.equal('fake-token');
  });

  it('Queries the user from the backend session, user is NOT logged in', async () => {
    mockGetRequest.returns({'username': ''});
    const username = await Auth.getUser();
    expect(username['username']).to.equal('');
  });

  it('Queries the user from the backend session, user is logged in', async () => {
    mockGetRequest.returns({'username': 'UABProvider'});
    const username = await Auth.getUser();
    expect(username['username']).to.equal('UABProvider');
  });
});

const test_token = {
  access_token: "fake-token",
  token_type: "bearer"
}