import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "@/assets/css/tailwind.css";
import "@/assets/css/animate.css";

Vue.config.productionTip = false;

Vue.prototype.speechSynthesis = window.speechSynthesis || {};
Vue.prototype.winNavigator = window.navigator || {};

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount("#app");
