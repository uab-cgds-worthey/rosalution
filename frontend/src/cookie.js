const cookie = {
  getCookie() {
    if (document.cookie == '') {
      return {};
    }

    const cookieValue = document.cookie.split(';')
        .find((row) => row.startsWith('DIVERGEN_TOKEN='))
        .split('=')[1];
    return cookieValue;
  },
  setCookie(token) {
    document.cookie = `DIVERGEN_TOKEN=${token}`;
  },
  removeCookie() {
    document.cookie = '';
  },
};

export {cookie};
