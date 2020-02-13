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
            params.append("institution", "w20_team6");
            params.append("username", credentials["username"]);
            params.append("password", credentials["password"]);
            params.append("grant_type", "password");
            params.append("scope", "query");
            return axios
                .post("https://api.clinc.ai/v1/oauth", params)
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
