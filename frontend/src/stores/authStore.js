import Auth from "../models/authentication";

const userStore = {
    state: {
        name: "User Store",
        username: "",
        email: "",
        roles: [],
    },
    async saveState() {
        const user = await Auth.fetchUser();
        this.state.name = user['name'];
        this.state.username = user['username'];
        this.state.email = user['email'];
    },
    getToken() {
        if(document.cookie == '') {
            return null;
        }

        const rosalutionCookie = document.cookie.split(';').find((row) => row.startsWith('rosalution_TOKEN='));
        
        if(typeof(rosalutionCookie) == 'undefined') {
            return null;
        }
        
        return rosalutionCookie.split('=')[1];
    },
    hasRole(role) {
        return this.state.roles.includes(role);
    },
}

export {userStore};