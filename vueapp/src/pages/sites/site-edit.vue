<template>
    <v-layout style="height:0" row justify-center>
        <v-dialog v-model="showEditSiteModal" @keydown.esc="$emit('close')" @keydown.enter="[changeSiteData(), $emit('close')]" persistent max-width="600px">
            <v-card>
                <v-card-title>
                    <span class="headline"> Edit your website </span>
                </v-card-title>
                <v-card-text>
                    <v-container>
                        <v-row>
                            <v-col cols="12" sm="6" md="6">
                                <v-text-field label="Site name*" v-model="site_edit.name" required></v-text-field>
                            </v-col>
                            <v-col cols="12">
                                <v-text-field label="URL" v-model="site_edit.url" required></v-text-field>
                            </v-col>
                        </v-row>
                    </v-container>
                    <small>*indicates required field</small>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="$emit('close')">Close</v-btn>
                    <v-btn color="blue darken-1" text @click="[changeSiteData(), $emit('close')]">
                        Edit Site
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-layout>
</template>

<script>
    import {mapActions, mapState} from "vuex";

    export default {
        name: "siteEdit",
        props: ['site', 'showEditSiteModal'],
        components: {},
        data() {
            return {
                site_edit: {
                    id: this.site.id,
                    name: null,
                    url: null,
                    ...this.site
                }
            }
        },
        mounted() {
        },
        computed: {
            ...mapState([""]),
        },
        methods: {
            ...mapActions(["siteChange","getSites"]),
            async changeSiteData() {
                await this.$store.dispatch('siteChange', {
                    id: this.site_edit.id,
                    name: this.site_edit.name,
                    url: this.site_edit.url,
                });
                console.log(this.site_edit.name);
                await this.getSites();
            }
        }
    }
</script>

<style scoped>

</style>