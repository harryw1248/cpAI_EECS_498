<template>
  <div>
      <section class="w-full flex-col items-center justify-center mt-32">
          <Login/>
      </section>
  </div>

</template>

<script>
import Login from "@/components/Login.vue";
export default {
  name: "Welcome",
  components: {
    Login
  }
};
</script>