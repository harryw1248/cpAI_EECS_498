<template>
    <div>
        <form @submit.prevent="sendUtterance">
            <label for="utterance" class="font-semibold">Utterance:</label>
            <input
                type="text"
                name="utterance"
                class="border w-full h-8"
                value
            />
            <button
                type="submit"
                name="button"
                class="mt-4 w-32 bg-blue-600 hover:bg-blue-500 text-center px-4 py-1 text-white font-semibold rounded-lg shadow-lg"
            >
                Send
            </button>
        </form>

        <div class="mt-16">
            <div class="font-semibold">Response:</div>
            <div class="border">
                <div
                    v-for="(value, name, index) in response"
                    v-bind:key="index"
                >
                    {{ name }}: {{ value }}
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "Converse",
    data() {
        return {
            response: "?"
        };
    },
    methods: {
        sendUtterance(e) {
            const token = JSON.parse(localStorage.getItem("user"))[
                "access_token"
            ];
            const headers = {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            };
            const data = {
                query: e.target.elements.utterance.value
            };

            console.log(headers); // eslint-disable-line no-console
            console.log(data); // eslint-disable-line no-console
            axios({
                method: "post",
                url: "https://api.clinc.ai/v1/query",
                headers,
                data
            })
                .then(response => {
                    console.log(response); // eslint-disable-line no-console
                    this.response = response.data;
                })
                .catch(e => {
                    alert("error - see console msg.");
                    console.log(e); // eslint-disable-line no-console
                });
        }
    }
};
</script>
