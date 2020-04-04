import axios from "axios";
import SpeechService from "@/services/SpeechService.js";
export const namespaced = true;

export const state = {
    loadingState: false,
    sttInProgress: false,
    sttResponse: "",
    history: [
        {
            id: 0,
            who: "CPai",
            text: "How may I help you?",
            timestamp: Date(),
            loadingState: false
        }
    ]
};

export const mutations = {
    ADD_TO_HISTORY(state, message) {
        state.history.push(message);
    },
    POP_FROM_HISTORY(state) {
        state.history.pop();
    },
    TOGGLE_LOADING(state) {
        state.loadingState = !state.loadingState;
    }
};

export const actions = {
    resetSession: ({ rootGetters }) => {
        axios({
            method: "get",
            url: rootGetters.getClientUrl + "reset"
        })
            .then(response => {
                console.log("reset client done", response);
                alert("Reset Dialogflow!");
            })
            .catch(e => {
                alert("error reset() request to the client - see console msg.");
                console.log(e); // eslint-disable-line no-console
            });
    },
    speak: ({ commit, dispatch, rootGetters }, message) => {
        commit("ADD_TO_HISTORY", {
            who: "You",
            text: message,
            timestamp: Date()
        });
        commit("TOGGLE_LOADING");

        axios({
            method: "post",
            url: rootGetters.getClientUrl + "query",
            headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            data: {
                query: message // e.target.elements.utterance.value
            }
        })
            .then(response => {
                dispatch("listen", response);
            })
            .catch(e => {
                alert("error - see console msg.");
                console.log(e); // eslint-disable-line no-console
            });
    },
    listen: ({ commit, dispatch }, response) => {
        console.log(response); // eslint-disable-line no-console
        dispatch("document/queryDocument", null, { root: true });

        commit("ADD_TO_HISTORY", {
            who: "CPai",
            text: response.data.responseText,
            intent: response.data.intent,
            timestamp: Date()
            //params: response.data.params
        });
        SpeechService.textToSpeech(response.data.responseText);
        commit("TOGGLE_LOADING");

        dispatch("displayForm1040", null, { root: true });
        //dispatch("updateForm1040", response.data.params, { root: true });
    }
};
