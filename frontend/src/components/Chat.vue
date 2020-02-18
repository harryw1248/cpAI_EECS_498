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
                    <p class="text-xs text-gray-700">
                        {{ message["timestamp"] }}
                    </p>
                </div>
                <div
                    v-if="message['who'] === 'CPai'"
                    class="flex flex-col items-end pr-4 py-1 self-end py-1 w-8/12 bg-blue-100 rounded"
                    v-on:click="debugModal = !debugModal"
                >
                    <p class="font-semibold">
                        {{ message["who"] }}
                    </p>
                    <p>
                        {{ message["text"] }}
                    </p>
                    <p class="text-xs text-gray-700">
                        {{ message["timestamp"] }}
                    </p>
                </div>
            </div>
        </section>
        <form @submit.prevent="sendUtterance" class="mt-4 h-16 flex">
            <label for="utterance" class="font-semibold"></label>
            <textarea
                type="text"
                name="utterance"
                class="resize-y border w-full rounded-lg py-2 px-4 outline-none text-xl"
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

function keepScrollDown() {
    const elem = document.getElementById("chat");
    elem.scrollTop = elem.scrollHeight - elem.clientHeight;
}

export default {
    name: "Chat",
    updated() {
        keepScrollDown();
    },
    data() {
        return {
            debugModal: false,
            messages: [
                {
                    id: 0,
                    who: "CPai",
                    text: "How may I help you?",
                    timestamp: Date.now()
                }
            ]
        };
    },
    methods: {
        sendUtterance(e) {
            this.messages.push({
                who: "You",
                text: e.target.elements.utterance.value,
                timestamp: Date.now()
            });

            const headers = {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            };

            const data = {
                query: e.target.elements.utterance.value
            };

            console.log(headers); // eslint-disable-line no-console
            axios({
                method: "post",
                url: "http://localhost:3000/query",
                headers,
                data
            })
                .then(response => {
                    console.log(response); // eslint-disable-line no-console
                    this.messages.push({
                        who: "CPai",
                        text: response.data,
                        timestamp: Date().now,
                        res: response.data
                    });
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
