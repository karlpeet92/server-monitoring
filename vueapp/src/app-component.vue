<template>
    <div id="app-layout">
        <router-view></router-view>
    </div>
</template>

<script>
    //import MainNavigation from './main-navigation.vue';

    import settings from "./settings";
    import {mapActions} from "vuex";

    export default {
        name: "layout",
        data() {
            return {};
        },
        mounted() {

        },
        methods: {}
    };
</script>

<style scoped></style>
