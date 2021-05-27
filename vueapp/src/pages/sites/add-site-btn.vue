<template>
    <v-layout style="height:100px; z-index:2" row justify-end v-if="index === 1">
        <v-dialog v-model="dialog" @keydown.esc="dialog=false" persistent max-width="600px">
            <template v-slot:activator="{ on }">
                <v-btn id="addNewSiteBtn" color="primary" dark v-on="on">Add New Site</v-btn>
            </template>
            <v-card>
                <v-card-title>
                    <span class="headline"> Add new website </span>
                </v-card-title>
                    <v-card-text>
                        <v-container>
                            <v-row>
                                <v-col cols="12" sm="6" md="6">
                                    <v-text-field label="Site name*" v-model="site_name" required></v-text-field>
                                </v-col>
                                <v-col cols="12">
                                    <v-text-field label="URL*" v-model="site_url" required></v-text-field>
                                </v-col>
                            </v-row>
                        </v-container>
                        <small>*indicates required field</small>
                    </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="dialog = false">Close</v-btn>
                    <v-btn color="blue darken-1" text v-on:click.prevent="siteData()" @click="dialog = false" >Add Site</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-layout>
</template>

<script>
    import { mapState, mapActions }    from "vuex";
    export default {
        name: "AddSiteBtn",
        props: ["site",],
        data: () => ({
            dialog: false,
            site_name: "",
            site_url: "",
            render: null,
        }),
        mounted() {

        },
        computed: {
            ...mapState(["index", "userID", "sites"])
        },
        methods: {
            ...mapActions(["newSite", "getSites"]),
            async siteData(event) {
                this.render ++;
                await this.$store.dispatch("newSite", {
                    site_name: this.site_name,
                     site_url: this.site_url,
                      user_id: this.userID,
                       render: this.render
                });
                this.site_name = this.site_url = "";
                await this.getSites();

            },
        }
    }
</script>

<style scoped>
    #addNewSiteBtn {
        margin-right: 40px;
    }
</style>