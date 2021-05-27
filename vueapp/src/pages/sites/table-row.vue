<template>
    <tbody>
        <tr v-for="site in sites" :key="'sr_'+site.id">
            <td>{{ site.name }}</td>
            <td>{{ site.id }}</td>
            <td>{{ site.url }}</td>
            <td>{{ site.created_at }}</td>
            <td><v-btn color="primary" href="javascript:{}" @click="connectSite(site)" style="height: 20px; width: 85px">Connect</v-btn></td>
            <td><a style="text-decoration:none;" href="javascript: {}" @click="editSite(site)">
                <v-icon v-text="'mdi-pencil'"></v-icon></a>
            </td>
            <td> <a style="text-decoration:none;" href="javascript: {}" @click="deleteSite(site)">
                <v-icon v-text="'mdi-trash-can'"></v-icon></a>
            </td>
        </tr>

        <site-connect :site="activeSite" v-if="showSiteConnectionModal"
                      :showSiteConnectionModal=Boolean @close="showSiteConnectionModal=false"/>
        <site-edit :site="activeSite" v-if="showEditSiteModal"
                   :showEditSiteModal=Boolean @close="showEditSiteModal=false"/>
        <site-delete :site="activeSite" v-if="showDeleteSiteModal"
                     :showDeleteSiteModal=Boolean @close="showDeleteSiteModal=false"/>
    </tbody>
</template>

<script>
    import SiteEdit                  from "./site-edit";
    import SiteDelete                from "./site-delete";
    import TableHead                 from "./table-head";
    import SiteConnect               from "./site-connect";
    import {mdiPencil, mdiTrashCan}  from "@mdi/js";
    import {mapState}                from "vuex";

    export default {
        name: "tableRow",
        props:["site"],
        components: {SiteEdit, SiteDelete, TableHead, SiteConnect},
        data() {
            return{
                showEditSiteModal: false,
                showDeleteSiteModal: false,
                showSiteConnectionModal: false,
                activeSite: {},

                icons: {
                    mdiPencil,
                    mdiTrashCan,
                },
            }
        },
        mounted() {
        },
        computed: {
            ...mapState(["sites"])
        },
        methods: {
            connectSite(site) {
                this.showSiteConnectionModal = true;
                this.activeSite = site;
            },
            editSite(site) {
                this.showEditSiteModal = true;
                this.activeSite = site;
            },
            deleteSite(site) {
                this.showDeleteSiteModal = true;
                this.activeSite = site;
            }
        }
    }
</script>

<style scoped>

</style>