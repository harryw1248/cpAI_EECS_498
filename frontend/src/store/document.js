import axios from "axios";
export const namespaced = true;

export const state = {
    user: {},
    spouse: {},
    dependents: Array(),
    dirtyBit: 0
};

export const mutations = {
    UPDATE_DATA: (state, data) => {
        const user = data["demographics"]["user"];
        const spouse = data["demographics"]["spouse"];
        const dependents = data["demographics"]["dependents"];

        for (const key of Object.keys(data["demographics"])) {
            state[key] = data["demographics"][key];
        }
        state.dirtyBit += 1;
    }
};

export const actions = {
    queryDocument({ commit }) {
        axios({
            method: "get",
            url: "http://localhost:5000/document"
        })
            .then(response => {
                console.log(response);
                commit("UPDATE_DATA", response.data);
            })
            .catch(e => {
                alert("error get() request to the backend - see console msg.");
                console.log(e); // eslint-disable-line no-console
            });
    }
};
