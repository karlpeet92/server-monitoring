import Vue from "vue";
import VueRouter from "vue-router";
import SiteData from "../pages/sites/sites.vue";

Vue.use(VueRouter);
let routes = [
    {
        path: "/",
        name: "sites",
        component: SiteData,
    }
];
let router = new VueRouter({
    mode: "history",
    base: "/",
    routes
});

export default router;
