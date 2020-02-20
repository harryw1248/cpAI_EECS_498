import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        userInfo: {
            firstName: "",
            lastName: "",
            address: {
                street: "",
                cityState: "",
                apt: null
            },
            filingStatus: "",
            ssn: {
                first: 0,
                second: 0,
                third: 0
            },
            foreignCountry: {
                country: "",
                state: "",
                po: 0
            }
        },
        logged: false,
        displayForm1040: false,
        count: 0
    },
    mutations: {
        /*
        SET_USER_DATA(state, userData) {
            state.user = userData;
            localStorage.setItem("user", JSON.stringify(userData));
            axios.defaults.headers.common[
                "Authorization"
            ] = `Bearer ${userData.access_token}`;
        },
        */
        toggleForm(state) {
            if (!state.displayForm1040) state.displayForm1040 = true;
        },
        SET_USER_DATA(state, userData) {
            console.log("before", state);
            Object.assign(state.userInfo, userData);
            console.log("after", state);
        }
    },
    actions: {
        /*
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
        },
        */
    },
    modules: {}
});
