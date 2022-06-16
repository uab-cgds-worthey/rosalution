const cookie = {
  getCookie() {
    if (document.cookie == '') {
      return {};
    }

    const cookieValue = document.cookie.split(';')
        .find((row) => row.startsWith('rosalution_TOKEN='))
        .split('=')[1];
    return cookieValue;
  },
  setCookie(token) {
    document.cookie = `rosalution_TOKEN=${token}`;
  },
  removeCookie() {
    document.cookie = '';
  },
};

export {cookie};
