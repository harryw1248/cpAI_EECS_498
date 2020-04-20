<template>
    <div class="grid grid-cols-5 gap-2 animated flip">
        <div class="col-span-2 flex justify-center">
            <Chat class="mt-12 mx-4" />
        </div>
        <div class="col-span-3 flex flex-col items-center">
            <img
                v-if="!showForm1040"
                src="../assets/logo.png"
                alt="CPai"
                class="mt-32 h-64"
            />
            <div v-if="!showForm1040">
                <div>Your Intelligent Accountant</div>
                <div>An Easy Way to Complete Your Taxes</div>
            </div>

            <a
                class="mt-4 ml-1 py-1 px-2 bg-blue-600 hover:bg-blue-500 text-center bg-gray-100 text-white font-semibold rounded-lg shadow-lg focus:outline-none"
                :href="backendUrl + 'pdf'"
            >
                Download the form as PDF
            </a>
            <img v-if="showForm1040" :src="formSrc" />
        </div>
    </div>
</template>

<script>
import Chat from "@/components/Chat.vue";
import { mapGetters, mapState } from "vuex";

export default {
    name: "Console",
    components: {
        Chat,
    },
    computed: {
        ...mapState({
            formSrc: (state) => state.document.formSrc,
            backendUrl: (state) => state.backendUrl,
        }),
        ...mapGetters({
            showForm1040: "isForm1040Toggled",
        }),
    },
};
</script>

<style scoped>
#form1040 {
    height: 100%;
}
</style>
