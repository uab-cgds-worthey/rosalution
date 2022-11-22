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

  it('Returns the rosalution_Token stored in the browsers document', () => {
    Object.defineProperty(window.document, 'cookie', {
      writable: true,
      value: 'rosalution_TOKEN=cookieomnomnom',
    });

    const expectedCookie = authStore.getToken();
    expect(expectedCookie).to.equal('cookieomnomnom');
  });

  it('Returns the rosalution_Token stored in the browsers document with lots of other cookies', () => {
    Object.defineProperty(window.document, 'cookie', {
      writable: true,
      // eslint-disable-next-line max-len
      value: '_gcl_au=gcl-au-fake; _ga_35R7WJH7GD=GS1.1.111111111.1.1.1111111111.0.0.0; screenResolution=1000x1000; rosalution_TOKEN=cookieomnomnom',
    });

    const expectedCookie = authStore.getToken();
    expect(expectedCookie).to.equal('cookieomnomnom');
  });

  it('Other cookies exist in the document, but not the rosalution token returns null', () => {
    Object.defineProperty(window.document, 'cookie', {
      writable: true,
      value: 'someOtherToken=notrosalutionlol',
    });

    const expectedCookie = authStore.getToken();

    expect(expectedCookie).to.equal(null);
  });

  it('No cookie exists and returns null when getting token', () => {
    Object.defineProperty(window.document, 'cookie', {
      writable: true,
      value: '',
    });

    const expectedCookie = authStore.getToken();

    expect(expectedCookie).to.equal(null);
  });

  it('Saves the state of the returned user object', async () => {
    authStore.saveState(userResponse);
    expect(authStore.state.full_name).to.equal(userResponse['full_name']);
    expect(authStore.state.username).to.equal(userResponse['username']);
    expect(authStore.state.email).to.equal(userResponse['email']);
  });

  it('Returns the roles a user has associated with them', () => {
    authStore.saveState(userResponse);

    expect(authStore.hasRole('developer')).to.equal(true);
  });

  it('Initiates a production login and recieves a bearer token', async () => {
    mockGetRequest.returns('fake-redirect-url');

    const expectedRedirectURL = await authStore.loginUAB();

    expect(expectedRedirectURL).to.equal('fake-redirect-url');
  });

  it('Initiates a development login and recieves a bearer token', async () => {
    mockPostLoginRequest.returns(accessTokenResponse);

    const userData = {'username': 'fakeUser', 'password': ''};
    const expectedUserData = await authStore.loginDevelopment(userData);

    expect(expectedUserData).to.equal(accessTokenResponse);
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

  it('Logs the user out and recieves a url for the CAS to expire the UAB session', async () => {
    mockGetRequest.returns({'url': 'fake.uab.padlock'});
    const expectedUrl = await authStore.logout();
    expect(expectedUrl['url']).to.equal('fake.uab.padlock');
  });
});

const userResponse = {
  'username': 'fakename',
  'full_name': 'Fake Name',
  'email': 'fakemail@fake.com',
  'scope': 'developer',
};

const accessTokenResponse = {
  access_token: 'fakeaccesstoken',
  token_type: 'bearer',
};
