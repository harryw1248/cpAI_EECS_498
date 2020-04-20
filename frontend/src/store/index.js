import Vue from "vue";
import Vuex from "vuex";
import * as document from "@/store/document.js";
import * as conversation from "@/store/conversation.js";

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        document,
        conversation,
    },
    state: {
        displayForm1040: false,
        logged: false,
        clientUrl: "http://localhost:3000/",
        backendUrl: "http://localhost:5000/",
        awsClient: false,
        awsBackend: false,
    },
    mutations: {
        SET_CUSTOM_BACKEND: (state, val) => {
            state.backendUrl = val;
            state.awsBackend = false;
        },
        TOGGLE_FORM1040_DISPLAY: (state) => {
            state.displayForm1040 = !state.displayForm1040;
        },
    },
    getters: {
        isForm1040Toggled: (state) => {
            return state.displayForm1040;
        },
        getClientUrl: (state) => {
            return state.clientUrl;
        },
        getBackendUrl: (state) => {
            return state.backendUrl;
        },
    },
    actions: {
        displayForm1040: ({ commit, state }) => {
            if (!state.displayForm1040) commit("TOGGLE_FORM1040_DISPLAY");
        },
    },
});
