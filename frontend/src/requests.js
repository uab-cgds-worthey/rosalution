import {cookie} from './cookie.js';
export default {
  async get(url) {
    const authToken = cookie.getCookie();
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + authToken,
      },
      mode: 'cors',
    });
    // Instead of throwing an error and halting operation, we're returning an object with
    // error that is handled in the respective methods that call this get function.
    if (response.status == 401) {
      return {'error': 'unauthorized'};
    }
    else if ( response.ok != true ) {
      throw new Error('Status Code: ' +response.status +' '+response.statusText);
    }
    return await response.json();
  },
  async post(url, data) {
    const response = await fetch(url, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      mode: 'cors',
      cache: 'no-cache',
      body: JSON.stringify({query: data}),
    });
    if ( response.ok != true ) {
      throw new Error('Status Code: ' +response.status +' '+response.statusText);
    }
    return await response.json();
  },
  // TODO: Need to find a way to craft the body of the request more elegantly
  // Needs to allow for granting specific scope types dynamically?
  async postLogin(url, data) {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      mode: 'cors',
      cache: 'no-cache',
      body: 'grant_type=password&scope=read+write&username=' + data.username + '&password=' + data.password,
    });

    return await response.json();
  },
  async postForm(url, data) {
    const formData = new FormData();

    const fieldEntries = Object.entries(data);
    for (const [field, fieldContent] of fieldEntries) {
      formData.append(field, fieldContent);
    }

    const response = await fetch(url, {
      method: 'POST',
      mode: 'cors',
      cache: 'no-cache',
      body: formData,
    });

    if ( response.ok != true ) {
      throw new Error('Status Code: ' +response.status +' '+response.statusText);
    }

    return await response.text();
  },
};
