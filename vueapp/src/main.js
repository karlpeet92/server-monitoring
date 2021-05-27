import Vue                  from 'vue';
import store                from "./store";
import router               from "./router";
import vuetify              from '@/plugins/vuetify';

import AppComponent         from "./app-component.vue";
import SiteData             from "./pages/sites/sites.vue";
import SiteTable            from "./pages/sites/sites-table.vue";
import UserRegForm          from "./pages/sites/user-reg-form.vue";
import LoginForm            from "./pages/sites/login-form.vue";
import AddSiteBtn           from "./pages/sites/add-site-btn.vue";
import SiteEdit             from "./pages/sites/site-edit.vue";
import SiteDelete           from "./pages/sites/site-delete.vue";
import TableRow             from "./pages/sites/table-row.vue";
import TableHead            from "./pages/sites/table-head.vue";
import SiteConnect          from "./pages/sites/site-connect.vue";
import Chart                from "./pages/sites/chart";
import ConnTable            from "./pages/sites/conn-table";
import MenuBtn              from "./pages/sites/menu-btn";
import PassChange           from "./pages/sites/pass-change";
import PassRepeat           from "./pages/sites/pass-repeat";

Vue.use(store, router);

let vueapp = new Vue({
    store,
    router,
    template: "<AppComponent/>",
    vuetify,

    components: {
        AppComponent,
        SiteData,
        SiteTable,
        UserRegForm,
        LoginForm,
        AddSiteBtn,
        SiteEdit,
        SiteDelete,
        TableRow,
        TableHead,
        SiteConnect,
        Chart,
        ConnTable,
        MenuBtn,
        PassChange,
        PassRepeat
    }
}).$mount("#app");
export default vueapp;

