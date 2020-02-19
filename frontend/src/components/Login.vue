<template>
    <div class="flex flex-col md:flex-row justify-center">
        <div class="w-10/12 lg:w-6/12 block md:flex md:shadow-lg rounded-lg">
            <div
                class="w-64 flex md:border-r border-gray-200 justify-center items-center"
            >
                <img src="../assets/logo.png" alt="CPai" class="h-32" />
            </div>
            <div class="w-full md:w-2/3 px-6 py-16">
                <div class="mb-4 font-light tracking-widest text-2xl">
                    Welcome to CPai
                </div>
                <div class="text-xs">
                    <div>*Not optimized for mobile screen (non-responsive)</div>
                </div>
                <form class="mt-6" @submit.prevent="login" autocomplete="on">
                    <div class="mt-4 flex flex-col items-start">
                        <label for="fusername" class="text-sm text-gray-800">
                            Username
                        </label>
                        <input
                            type="text"
                            name="username"
                            id="username"
                            class="focus:border-blue-600 appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none"
                            autocomplete="username"
                            required
                        />
                    </div>
                    <div class="mt-4 flex flex-col items-start">
                        <label for="password" class="text-sm text-gray-800">
                            Your password
                        </label>
                        <input
                            type="password"
                            name="password"
                            id="password"
                            class="focus:border-blue-600 appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none"
                            autocomplete="current-password"
                            required
                        />
                    </div>
                    <div class="block md:flex items-center justify-center mt-8">
                        <button
                            type="submit"
                            class="w-32 bg-blue-600 hover:bg-blue-500 text-center px-4 py-2 text-white font-semibold rounded-lg shadow-lg"
                        >
                            Login
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "Login",
    methods: {
        login(e) {
            /*
        this.$store
            .dispatch("login", {
                username: e.target.elements.username.value,
                password: e.target.elements.password.value
            })
            .then(() => {
                this.$router.push({ name: "Console" });
            });
       */
            console.log(e);
            this.$router.push({ name: "Console" });
        }
    }
};
</script>
