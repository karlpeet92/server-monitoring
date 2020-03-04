import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import settings from "@/settings";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        message: "Tere Default"
    },
    mutations: {
        changeMessage(state, message) {
            state.message = message;
        }
    },
    actions: {
        async getSites({commit}, payload) {
            let response = await axios.post(settings.api_url + "/user-site", {});
        }
    }
});