<template>
    <div class="grid grid-cols-5 gap-2">
        <div class="col-span-2 flex justify-center">
            <Chat class="mt-12 mx-4" />
            <!--<Converse class="w-9/12 mt-32" />-->
        </div>
        <div class="col-span-3">
            <Form1040 class="border border-blue-600 mt-8 h-64 bg-blue-100 mx-2"> </Form1040>
        </div>
    </div>
</template>

<script>
import Chat from "@/components/Chat.vue";
import Form1040 from "@/components/Form1040.vue";
//import Converse from "@/components/Converse.vue";

export default {
  name: "Console",
  components: {
    Chat,
    //Converse,
    Form1040
  }
};
</script>
