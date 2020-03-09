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
                {{ showForm1040 }}
            </div>

            <Form1040
                v-if="showForm1040"
                id="form1040"
                class="border w-full border-gray mt-8 bg-blue-100 mx-2 animated bounceInDown slower"
                style="overflow-y: auto; position: relative;"
            >
            </Form1040>
        </div>
    </div>
</template>

<script>
import Chat from "@/components/Chat.vue";
import Form1040 from "@/components/Form1040.vue";
import { mapGetters } from "vuex";

export default {
  name: "Console",
  components: {
    Chat,
    Form1040
  },
  computed: {
    ...mapGetters({
      showForm1040: "isForm1040Toggled"
    })
  }
};
</script>

<style scoped>
#form1040 {
  height: 100%;
}
</style>
