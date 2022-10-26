import {authStore} from '@/stores/authStore.js';

export default {
  async get(url) {
    const authToken = authStore.getToken();
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
    } else if ( response.ok != true ) {
      throw new Error('Status Code: ' +response.status +' '+response.statusText);
    }
    return await response.json();
  },
  async post(url, data) {
    const authToken = authStore.getToken();
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + authToken,
      },
      mode: 'cors',
      cache: 'no-cache',
      body: JSON.stringify(data),
    });
    const content = await response.json();
    if ( response.ok != true ) {
      throw new Error('Status Code: ' +response.status +' '+response.statusText + '\n' + JSON.stringify(content));
    }
    return content;
  },
  async put(url, data) {
    const authToken = authStore.getToken();
    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + authToken,
      },
      mode: 'cors',
      cache: 'no-cache',
      body: JSON.stringify(data),
    });
    const content = await response.json();
    if ( response.ok != true ) {
      throw new Error('Status Code: ' +response.status +' '+response.statusText + '\n' + JSON.stringify(content));
    }
    return content;
  },
  async postLogin(url, data) {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      mode: 'cors',
      cache: 'no-cache',
      body: 'grant_type=password&username=' + data.username + '&password=secret',
    });

    return await response.json();
  },
  async postForm(url, data) {
    const authToken = authStore.getToken();

    const formData = new FormData();
    const fieldEntries = Object.entries(data);
    for (const [field, fieldContent] of fieldEntries) {
      formData.append(field, fieldContent);
    }
    const response = await fetch(url, {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Authorization': 'Bearer ' + authToken,
      },
      cache: 'no-cache',
      body: formData,
    });
    if ( response.ok != true ) {
      throw new Error('Status Code: ' +response.status +' '+response.statusText);
    }
    return await response.json();
  },
  async delete(url) {
    const authToken = authStore.getToken();
    const response = await fetch(url, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + authToken,
      },
      mode: 'cors',
      cache: 'no-cache',
    });

    if ( response.ok != true ) {
      console.log(response);
      throw new Error(`Status Code: ${response.status} ${ response.statusText}\nURL: \n${response.url}`);
    }

    if ( response.bodyUsed) {
      return await response.json();
    }

    return response.ok;
  },
};
