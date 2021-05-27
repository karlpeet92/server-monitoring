<template >
<div id="vueapp">
    <v-app id="inspire">
        <v-app-bar app clipped-right style="height:75px" color="blue-grey" dark>
            <v-toolbar-title style="margin-top: 25px; margin-left: 25px">Server Monitor</v-toolbar-title>
            <v-spacer />
        <menu-btn style="margin-top: 10px" />
        </v-app-bar>
        <span style="margin-top: 80px; margin-left: 40px" v-if="index === 1">Your Account ID: {{ userID }}</span>
        <site-table style="margin-top: 20px; margin-left: 10px" />
        <br />
        <br />
        <br />
            <user-reg-form />
        <br />
        <br />
        <br />
            <login-form />
            <add-site-btn />
        <v-footer app color="blue-grey" class="white--text" style="height: 35px; padding:0" />
    </v-app>
</div>
</template>
<script>
    import {mapActions, mapState} from "vuex";
    import SiteTable              from "./sites-table";
    import UserRegForm            from "./user-reg-form";
    import LoginForm              from "./login-form";
    import AddSiteBtn             from "./add-site-btn";
    import MenuBtn                from "./menu-btn";

    export default {
        name: "SiteData",
        components: {
            SiteTable,
            UserRegForm,
            LoginForm,
            AddSiteBtn,
            MenuBtn
        },
        props: {
            source: String
        },
        data: () => ({
            dialog: false
        }),
        mounted() {
        },
        computed: {
            ...mapState(['sites', "userID", "index"]),
        },
        methods: {
            ...mapActions(['getSites']),
        }
    }
</script>