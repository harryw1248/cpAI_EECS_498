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
//import SpeechService from "@/services/SpeechService.js";

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
  computed: mapState({
    messages: state => state.conversation.history
  }),
  methods: {
    /*speechToTextOn() {
            SpeechService.startStream();
        },
        speechToTextOff() {
            SpeechService.stopStream();
        },*/
    sendUtterance(e) {
      const utterance = e.target.elements.utterance.value;
      this.$store.dispatch("conversation/speak", utterance);
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
