import {authStore} from '@/stores/authStore.js';

/**
 * Sends the form data either 'POST' or 'PUT method
 * @param {string} method 'POST' or 'PUT'
 * @param {string} url The url to send the data too
 * @param {Object} data form data to send
 * @return {Object} the JSON body of response
 */
async function sendFormData(method, url, data) {
  const authToken = authStore.getToken();

  const formData = new FormData();
  const fieldEntries = Object.entries(data);
  for (const [field, fieldContent] of fieldEntries) {
    formData.append(field, fieldContent);
  }
  const response = await fetch(url, {
    method: method,
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
}

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
  async getFile(url, data) {
    const authToken = authStore.getToken();
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + authToken,
      },
      mode: 'cors',
    }).then((res) => {return res.blob(); }).then((result) => {
      var a = document.createElement("a");
      a.href = window.URL.createObjectURL(result);
      a.download = data.filename;
      a.click();
    });
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
    return await sendFormData('POST', url, data);
  },
  async putForm(url, data) {
    return await sendFormData('PUT', url, data);
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
