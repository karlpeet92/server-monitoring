<template>
    <v-simple-table v-if="index === 1">
        <template v-slot:default>
            <table-head :key="componentKey"/>
            <table-row />
        </template>
    </v-simple-table>
</template>

<script>

    import TableRow                      from "./table-row";
    import TableHead                     from "./table-head";
    import {mapActions, mapState}        from "vuex";

    export default {
        name: "siteTable",
        components: {
            TableRow,
            TableHead,
        },
        data() {
            return{
                componentKey: this.renderIdx
            }
        },
        mounted() {

        },
        computed: {
            ...mapState(["sites", "renderIdx", "index"])
        },
        methods: {
        }
    }
</script>

<style scoped>

</style>

