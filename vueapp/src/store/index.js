import Vue           from "vue";
import Vuex          from "vuex";
import axios         from "axios";
import settings      from "@/settings";
import UserRegForm   from "../pages/sites/user-reg-form.vue";
import LoginForm     from "../pages/sites/login-form.vue";
import AddSiteBtn    from "../pages/sites/add-site-btn.vue";
import MenuBtn       from "../pages/sites/menu-btn.vue";
import PassRepeat    from "../pages/sites/pass-repeat.vue";
import PassChange    from "../pages/sites/pass-change.vue";

Vue.use(Vuex);

const vuexStore = new Vuex.Store({
    components: {UserRegForm, LoginForm, AddSiteBtn, MenuBtn, PassRepeat, PassChange},
    state: {
        sites: [],
        userEmail: "",
        index: null,
        userID: null,
        renderIdx: 0,
        emailPass: Boolean,
        pass: Boolean,
        checkPass: Boolean
    },
    mutations: {
        setSites(state, sites) {
            state.sites = sites;
        },
        userEmail(state, userEmail) {
            state.userEmail = userEmail
        },
        index(state, index){
            state.index = index
        },
        passEmail(state, e_pass) {
            state.emailPass = e_pass
        },
        pass(state, pass_pass) {
            state.pass = pass_pass
        },
        checkPass(state, pass_pass) {
            state.checkPass = pass_pass
        },
        userId(state, userID){
            state.userID = userID
        },
        renderIndex(state, renderIdx){
            state.renderIdx = renderIdx
        },
        logoutIdx(state, payload){
            state.index = payload.idx
        },
    },
    actions: {
        async getSites({commit, state}, payload) {
            let response = await axios.get(settings.api_url + "/user-site", {
                params: {
                    user_id: state.userID
                }
            });
            commit("setSites", response.data);
        },
        async register({commit}, payload) {
            let response = await axios.post(settings.assets_url + "/user", payload);
            commit("index", response.data.success);
            commit("userId", response.data.user.id);
            commit("userEmail", payload.email);
        },
        async login({commit}, payload) {
            let response = await axios.post(settings.assets_url + "/user", payload);
            commit("index", response.data.success);
            commit("userId", response.data.id);
            commit("userEmail", payload.email);
            commit("passEmail", response.data.email_pass);
            commit("pass", response.data.pass_pass);
        },
        async passCheck({commit}, payload){
            let response = await axios.post(settings.assets_url + "/user", payload);
            commit("checkPass", response.data.pass_pass);
            console.log(response.data.pass_pass)
        },
        async newSite({commit}, payload) {
            let user_site_response = await axios.post(settings.api_url + "/user-site", payload);
            commit('renderIndex', payload.render);
        },
        async siteChange({commit}, payload) {
            await axios.post(settings.assets_url + "/site", payload);
        },
        async siteDelete({commit}, payload) {
            let response =  await axios.delete(settings.api_url + "/user-site", {
                params: {
                    site_id: payload.id
                }
            });
        },
    }
});

export default vuexStore;
