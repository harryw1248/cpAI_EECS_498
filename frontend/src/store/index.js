import Vue from "vue";
import Vuex from "vuex";
import * as form1040 from "@/store/form1040.js";
import * as conversation from "@/store/conversation.js";

Vue.use(Vuex);

const parse = param => {
    if (!param) return null;
    if (param["kind"] === "stringValue") {
        if (param["stringValue"] === "yes") return true;
        if (param["stringValue"] === "no") return false;
        return param["stringValue"];
    } else if (param["kind"] === "numberValue") {
        return param["numberValue"];
    }
    return null;
};

export default new Vuex.Store({
    modules: {
        form1040,
        conversation
    },
    state: {
        formData: {},
        dirtyBit: 0,
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
        UPDATE_FORM_DATA: (state, params) => {
            for (const key of Object.keys(params)) {
                state.formData[key] = parse(params[key]);
            }
            state.dirtyBit += 1;
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
        updateForm1040: ({ commit }, params) => {
            commit("UPDATE_FORM_DATA", params);
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
