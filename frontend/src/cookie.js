const cookie = {
    setCookie(token) {
        document.cookie = `DIVERGEN_TOKEN=${token}`;
    },
    getCookie() {
        console.log(document.cookie)
        if(document.cookie == '')
            return {}
        
        const cookieValue = document.cookie.split(';')
            .find(row => row.startsWith('DIVERGEN_TOKEN='))
            .split('=')[1];
        return cookieValue
    },
};

export { cookie };