import { reactive } from "vue";

export const userStore = reactive({
    state: {
        token: {},
    },

    async saveState(token) {
        this.state.token = token;
    },
    getState() {
        return this.state;
    }
});

// const userStore = {
//     state: {
//         token: {},
//     },

//     async saveState(token) {
//         this.state.token = token;
//     }
// };

// export { userStore };
