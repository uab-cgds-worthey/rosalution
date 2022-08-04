const cookie = {
  getCookie() {
    if (document.cookie == '') {
      return {};
    }

    const rosalutionCookie = document.cookie.split(';')
      .find((row) => row.startsWith('rosalution_TOKEN='))
    if( typeof(rosalutionCookie) == 'undefined' ) {
      return {};
    }
    return rosalutionCookie.split('=')[1];
  },
  setCookie(token) {
    document.cookie = `rosalution_TOKEN=${token}`;
  },
  removeCookie() {
    document.cookie = '';
  },
};

export {cookie};
