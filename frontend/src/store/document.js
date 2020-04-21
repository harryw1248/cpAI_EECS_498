export const namespaced = true;

export const state = {
    formSrc: "",
    user: {},
    spouse: {},
    dependents: Array(),
    user_income: {},
    dirtyBit: 0,
};

export const mutations = {
    UPDATE_DATA: (state, data) => {
        const user = data["demographics"]["user"];
        const spouse = data["demographics"]["spouse"];
        const dependents = data["demographics"]["dependents"];
        state["user_income"] = data["income"]["user"];

        for (const key of Object.keys(data["demographics"])) {
            state[key] = data["demographics"][key];
        }
        state.dirtyBit += 1;
    },
};

export const actions = {
    queryDocument({ commit, state, rootGetters }) {
        const token = new Date().getTime();
        state.formSrc = rootGetters.getBackendUrl + "jpg?time+" + token;
    },
};
