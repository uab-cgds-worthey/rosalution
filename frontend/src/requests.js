import {userStore} from './authStore.js';

export default {
  async get(url) {
    const authToken = userStore.getState();
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + authToken.token,
      },
      mode: 'cors',
    });
    if ( response.ok != true ) {
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
