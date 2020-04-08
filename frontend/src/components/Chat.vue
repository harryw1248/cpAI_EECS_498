<template>
    <div class="w-full h-screen">
        Chat History

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
                v-model="sttResponse"
                required
            />
            <button
                type="submit"
                name="button"
                class="ml-1 w-16 bg-blue-600 hover:bg-blue-500 text-center bg-gray-100 text-white font-semibold rounded-lg shadow-lg focus:outline-none"
            >
                Send
            </button>

            <button
                name="button"
                class="ml-1 w-16 bg-blue-600 hover:bg-blue-500 text-center bg-gray-100 text-white font-semibold rounded-lg shadow-lg focus:outline-none"
                v-if="!sttInProgress"
                @click="speechToTextOn"
            >
                <svg
                    class="mx-auto"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="white"
                    width="32px"
                    height="32px"
                >
                    <path
                        d="M12 14c1.66 0 2.99-1.34 2.99-3L15 5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm-1.2-9.1c0-.66.54-1.2 1.2-1.2.66 0 1.2.54 1.2 1.2l-.01 6.2c0 .66-.53 1.2-1.19 1.2-.66 0-1.2-.54-1.2-1.2V4.9zm6.5 6.1c0 3-2.54 5.1-5.3 5.1S6.7 14 6.7 11H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c3.28-.48 6-3.3 6-6.72h-1.7z"
                    />
                    <path d="M0 0h24v24H0z" fill="none" />
                </svg>
            </button>
            <button
                name="button"
                class="ml-1 w-16 bg-blue-600 hover:bg-blue-500 text-center bg-gray-100 text-white font-semibold rounded-lg shadow-lg focus:outline-none"
                v-if="sttInProgress"
                @click="speechToTextOff"
            >
                <svg
                    class="mx-auto"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="red"
                    width="30px"
                    height="30px"
                >
                    <path d="M24 24H0V0h24v24z" fill="none" />
                    <circle cx="12" cy="12" r="8" />
                </svg>
            </button>
        </form>
        <div></div>
        <div class="text-gray-400 mt-8 hidden">
            Aws-client
            <input type="checkbox" id="awsclient" v-model="awsClient" />
            Aws-backend
            <input type="checkbox" id="awsbackend" v-model="awsBackend" />
            <button
                name="button"
                class="mt-2 ml-1 w-16 bg-gray-300 hover:bg-blue-500 text-center bg-gray-100 text-white font-semibold rounded-lg shadow-lg focus:outline-none"
                @click="handleResetSession"
            >
                Reset
            </button>
        </div>
        <div class="mx-auto mt-6 hidden">
            <input class="w-full border" type="text" v-model="backendUrl" />
        </div>
        <!--<button
            name="button"
            class="mt-2 ml-1 w-16 bg-blue-600 hover:bg-blue-500 text-center bg-gray-100 text-white font-semibold rounded-lg shadow-lg focus:outline-none"
            @click="speechToTextOn"
        >
            Stream Speech
        </button>
        <button
            name="button"
            class="mt-2 ml-1 w-16 bg-blue-600 hover:bg-blue-500 text-center bg-gray-100 text-white font-semibold rounded-lg shadow-lg focus:outline-none"
            @click="speechToTextOff"
        >
            Stop Stream</button
        >-->
    </div>
</template>

<script>
import BeatLoader from "vue-spinner/src/PulseLoader.vue";
import { mapState } from "vuex";
import SpeechService from "@/services/SpeechService.js";

function keepScrollDown() {
    const elem = document.getElementById("chat");
    elem.scrollTop = elem.scrollHeight - elem.clientHeight;
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
    computed: {
        awsClient: {
            get() {
                return this.$store.state.awsClient;
            },
            set(value) {
                this.$store.commit("TOGGLE_AWS_CLIENT", value);
            }
        },
        awsBackend: {
            get() {
                return this.$store.state.awsBackend;
            },
            set(value) {
                this.$store.commit("TOGGLE_AWS_BACKEND", value);
            }
        },
        backendUrl: {
            get() {
                return this.$store.state.backendUrl;
            },
            set(value) {
                this.$store.commit("SET_CUSTOM_BACKEND", value);
            }
        },
        ...mapState({
            messages: state => state.conversation.history,
            sttInProgress: state => state.conversation.sttInProgress,
            sttResponse: state => state.conversation.sttResponse
        })
    },
    methods: {
        speechToTextOn() {
            SpeechService.startSpeaking();
        },
        speechToTextOff() {
            //SpeechService.stopStream();
            return;
        },
        handleResetSession() {
            this.$store.dispatch("conversation/resetSession");
        },
        sendUtterance(e) {
            const utterance = e.target.elements.utterance.value;
            this.$store.dispatch("conversation/speak", utterance);
            e.target.elements.utterance.value = null;
        }
    },
    created() {
        SpeechService.initSpeechToText();
    }
};
</script>

<style scoped>
#chat {
    min-height: 30%;
    max-height: 70%;
}
</style>
