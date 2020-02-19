import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        user: null
    },
    mutations: {
        SET_USER_DATA(state, userData) {
            state.user = userData;
            localStorage.setItem("user", JSON.stringify(userData));
            axios.defaults.headers.common[
                "Authorization"
            ] = `Bearer ${userData.access_token}`;
        }
    },
    actions: {
        login({ commit }, credentials) {
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
        }
    },
    modules: {}
});
