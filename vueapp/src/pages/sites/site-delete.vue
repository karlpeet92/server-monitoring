<template>
    <v-layout style="height:0px;" row justify-center>
        <v-dialog v-model="showDeleteSiteModal" @keydown.esc="$emit('close')" @keydown.enter="[deleteSite(), $emit('close')]" persistent max-width="600px">
            <v-card>
                <v-card-title>
                    <span class="headline"> Would you like to delete your website? </span>
                </v-card-title>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="[deleteSite(), $emit('close')]">
                        YES
                    </v-btn>
                    <v-btn color="blue darken-1" text @click="$emit('close')" >NO</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-layout>
</template>

<script>
    import {mapActions, mapState}   from "vuex";

    export default {
        name: "site-delete",
        props: ["site", "showDeleteSiteModal"],
        data() {
            return {
                id: this.site.id,
                index: this.site.index,
                ...this.site
            }
        },
        mounted() {
        },
        computed: {
            ...mapState(["sites"]),
        },
        methods: {
            ...mapActions(["siteDelete", "getSites"]),
            async deleteSite() {
                await this.$store.dispatch("siteDelete",{
                   id: this.id
                });
                let idx = this.sites.indexOf(this.site);
                await this.getSites()
            }
        }
    }
</script>

<style scoped>

</style>