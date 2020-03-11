import Vue from "vue";
import Vuex from "vuex";
import * as document from "@/store/document.js";
import * as conversation from "@/store/conversation.js";

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        document,
        conversation
    },
    state: {
        displayForm1040: false,
        logged: false
    },
    mutations: {
        SET_USER_DATA: (state, userData) => {
            /*
            state.user = userData;
            localStorage.setItem("user", JSON.stringify(userData));
            axios.defaults.headers.common[
                "Authorization"
            ] = `Bearer ${userData.access_token}`;
            */
        },
        TOGGLE_FORM1040_DISPLAY: state => {
            state.displayForm1040 = !state.displayForm1040;
        }
    },
    getters: {
        isForm1040Toggled: state => {
            return state.displayForm1040;
        }
    },
    actions: {
        displayForm1040: ({ commit, state }) => {
            if (!state.displayForm1040) commit("TOGGLE_FORM1040_DISPLAY");
        },
        login: ({ commit }, credentials) => {
            /*
            const params = new URLSearchParams();
            params.append("username", credentials["username"]);
            params.append("password", credentials["password"]);
            return axios
                .post("http://localhost:3000/", params)
                .then(response => {
                    console.log(response); // eslint-disable-line no-console
                    commit("SET_USER_DATA", response.data);
                })
                .catch(e => {
                    alert("error - see console msg.");
                    console.log(e);
                });
            */
        }
    }
});
