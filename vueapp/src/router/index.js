import Vue from "vue";
import VueRouter from "vue-router";
import SitesPage from "../pages/sites/sites.vue";

Vue.use(VueRouter);
let routes = [
    {
        path: "/",
        name: "sites",
        component: SitesPage,
    }
];
let router = new VueRouter({
    mode: "history",
    base: "/",
    routes
});

export default router;
