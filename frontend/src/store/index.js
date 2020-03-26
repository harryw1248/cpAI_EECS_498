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
        logged: false,
        clientUrl:
            "http://ec2-18-191-149-72.us-east-2.compute.amazonaws.com:3000/",
        backendUrl:
            "http://ec2-18-220-141-233.us-east-2.compute.amazonaws.com:5000/document",
        awsClient: true,
        awsBackend: true
    },
    mutations: {
        SET_CUSTOM_BACKEND: (state, val) => {
            state.backendUrl = val;
            state.awsBackend = false;
        },
        TOGGLE_FORM1040_DISPLAY: state => {
            state.displayForm1040 = !state.displayForm1040;
        },
        TOGGLE_AWS_CLIENT: (state, val) => {
            if (val) {
                state.clientUrl =
                    "http://ec2-18-191-149-72.us-east-2.compute.amazonaws.com:3000/";
                state.awsClient = true;
            } else {
                state.clientUrl = "http://localhost:3000/";
                state.awsClient = false;
            }
        },
        TOGGLE_AWS_BACKEND: (state, val) => {
            if (val) {
                state.backendUrl =
                    "http://ec2-18-220-141-233.us-east-2.compute.amazonaws.com:5000/document";
                state.awsBackend = true;
            } else {
                state.backendUrl = "http://localhost:5000/document";
                state.awsBackend = false;
            }
        }
    },
    getters: {
        isForm1040Toggled: state => {
            return state.displayForm1040;
        },
        getClientUrl: state => {
            console.log(state.clientUrl);
            return state.clientUrl;
        },
        getBackendUrl: state => {
            return state.backendUrl;
        }
    },
    actions: {
        displayForm1040: ({ commit, state }) => {
            if (!state.displayForm1040) commit("TOGGLE_FORM1040_DISPLAY");
        }
    }
});
