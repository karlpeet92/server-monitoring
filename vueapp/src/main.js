import Vue from 'vue';
import store from "./store";
import router from "./router";
import AppComponent from "./app-component.vue";

let vueapp = new Vue({
    store,
    router,
    template: "<AppComponent/>",
    components: {AppComponent}

}).$mount("#app");
export default vueapp;
