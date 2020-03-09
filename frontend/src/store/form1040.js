/*
export const namespaced = true;

export const state = {
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
};

export const mutations = {
    SET_USER_DATA(state, userData) {
        console.log("before", state);
        Object.assign(state.userInfo, userData);
        console.log("after", state);
    }
};
*/
export const actions = {
    /*
    fillInUserData(data) {
        const retData = {};
        if (data["given-name"]) {
            retData["firstName"] = data["given-name"];
        }
        if (data["last-name"]) {
            retData["lastName"] = data["last-name"];
        }
        if (data["social_security"]) {
            retData["ssn"] = {
                first: data["social_security"].slice(0, 3),
                second: data["social_security"].slice(3, 6),
                third: data["social_security"].slice(6, 9)
            };
        }
        if (data["location"]) {
            retData["address"] = {
                street: data["location"]["street-address"]["stringValue"],
                cityState:
                    data["location"]["city"]["stringValue"] +
                    " " +
                    data["location"]["admin-area"]["stringValue"] +
                    " " +
                    data["location"]["zip-code"]["stringValue"]
            };
        }
        return retData;
    }*/
};
