import Vue from "vue";
import VueRouter from "vue-router";
Vue.use(VueRouter);

const routes = [
    {
        path: "/",
        name: "Welcome",
        redirect: { name: "Console" },
    },
    {
        path: "/console",
        name: "Console",
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () =>
            import(/* webpackChunkName: "about" */ "../views/Console.vue"),
    },
];

const router = new VueRouter({
    routes,
});

export default router;
