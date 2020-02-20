<template>
    <div class="w-full h-screen">
        Chat History
        <div v-if="this.debugModal">
            asdfas
        </div>
        <section id="chat" class="overflow-y-auto py-4 px-2 mt-2 rounded">
            <div
                v-for="(message, index) in messages"
                v-bind:key="index"
                class="flex flex-col mt-4"
            >
                <div
                    v-if="message['who'] === 'You'"
                    class="flex flex-col py-1 items-start pl-4 w-8/12 bg-gray-100 rounded"
                >
                    <p class="font-semibold">
                        {{ message["who"] }}
                    </p>
                    <p>
                        {{ message["text"] }}
                    </p>
                    <p class="pt-2 text-xs text-gray-700">
                        {{ message["timestamp"] }}
                    </p>
                </div>
                <div
                    v-if="message['who'] === 'CPai'"
                    class="flex flex-col items-end pr-4 self-end pl-2 py-1 w-8/12 bg-blue-100 rounded"
                    v-on:click="debugModal = !debugModal"
                >
                    <p v-if="message['loadingState']">
                        <beat-loader></beat-loader>
                    </p>
                    <p v-if="!message['loadingState']" class="font-semibold">
                        {{ message["who"] }}
                    </p>
                    <p class="">
                        {{ message["text"] }}
                    </p>
                    <p class="mt-2 text-xs text-gray-700">
                        {{ message["timestamp"] }}
                    </p>
                </div>
            </div>
        </section>
        <form @submit.prevent="sendUtterance" class="mt-4 h-16 flex">
            <label for="utterance" class="font-semibold"></label>
            <input
                type="text"
                name="utterance"
                class="resize-y w-full px-4 outline-none text-xl border-b-2 border-blue-400"
                placeholder="Enter your response"
                required
            />
            <button
                type="submit"
                name="button"
                class="ml-1 w-16 bg-blue-600 hover:bg-blue-500 text-center bg-gray-100 text-white font-semibold rounded-lg shadow-lg focus:outline-none"
            >
                Send
            </button>
        </form>
    </div>
</template>

<script>
import axios from "axios";
import BeatLoader from "vue-spinner/src/PulseLoader.vue";

function keepScrollDown() {
    const elem = document.getElementById("chat");
    elem.scrollTop = elem.scrollHeight - elem.clientHeight;
}

function fillInUserData(data) {
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
}

export default {
    name: "Chat",
    components: {
        /* eslint-disable vue/no-unused-components */
        BeatLoader
    },
    updated() {
        keepScrollDown();
    },
    data() {
        return {
            debugModal: false,
            formDisplay: false,
            messages: [
                {
                    id: 0,
                    who: "CPai",
                    text: "How may I help you?",
                    timestamp: Date(),
                    loadingState: false
                }
            ]
        };
    },
    methods: {
        sendUtterance(e) {
            this.messages.push({
                who: "You",
                text: e.target.elements.utterance.value,
                timestamp: Date()
            });

            const headers = {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            };

            const data = {
                query: e.target.elements.utterance.value
            };

            this.messages.push({
                who: "CPai",
                loadingState: true
            });

            console.log(headers); // eslint-disable-line no-console
            axios({
                method: "post",
                url: "http://localhost:3000/query",
                headers,
                data
            })
                .then(response => {
                    console.log(response); // eslint-disable-line no-console
                    let responseData = response.data;
                    this.messages.pop();
                    this.messages.push({
                        who: "CPai",
                        text: responseData.responseText,
                        timestamp: Date(),
                        res: responseData,
                        loadingState: false
                    });

                    const newUserData = fillInUserData(responseData.data);
                    this.$store.commit("SET_USER_DATA", newUserData);
                    if (!this.formDisplay) {
                        this.$store.commit("toggleForm");
                    }
                })
                .catch(e => {
                    alert("error - see console msg.");
                    console.log(e); // eslint-disable-line no-console
                });

            e.target.elements.utterance.value = null;
        }
    }
};
</script>

<style scoped>
#chat {
    min-height: 30%;
    max-height: 70%;
}
</style>
