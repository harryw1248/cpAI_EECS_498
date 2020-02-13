<template>
    <div class="flex flex-col justify-center items-center">
        <Converse class="w-9/12 mt-32" />

        <Form1040 class="border border-blue-600 mt-32"> </Form1040>
    </div>
</template>

<script>
// @ is an alias to /src
import Form1040 from "@/components/Form1040.vue";
import Converse from "@/components/Converse.vue";

export default {
    name: "Console",
    components: {
        Converse,
        Form1040
    }
};
</script>
