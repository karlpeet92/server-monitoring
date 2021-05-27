<template>
    <v-layout row justify-center v-if="checkPass === true">
        <v-dialog v-model="openPassChange" @keydown.esc="$emit('close')" @keydown.enter="passChange()" persistent max-width="600px">
            <v-card >
                <v-card-title>
                    <span class="headline">Change Password</span>
                </v-card-title>
                    <v-card-text>
                        <v-container>
                            <v-row>
                                <v-col cols="12">
                                    <v-text-field hide-details label="Enter new password" v-model="password" type="password" required></v-text-field>
                                </v-col>
                                <v-col cols="12">
                                    <v-text-field hide-details label="Repeat password" v-model="re_password" type="password" required></v-text-field>
                                    <span v-if="repeatError === true" style="color: red">Repeated passwords is incorrect</span>
                                </v-col>
                            </v-row>
                        </v-container>
                    </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="$emit('close')">Close</v-btn>
                    <v-btn color="blue darken-1" text @click="passChange()">Change</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-layout>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        name: "pass-change",
        props: ['showPassChange'],
        data() {
            return {
                password: '',
                re_password: '',
                repeatError: Boolean,
                openPassChange: this.showPassChange
            }
        },
        mounted() {
        },
        computed: {
            ...mapState(['checkPass', 'userEmail'])
        },
        methods: {
            async passChange () {
                 if (this.password === this.re_password) {
                     await this.$store.dispatch("passCheck", {
                         form: "password_change",
                         password: this.password,
                         email: this.userEmail
                     });
                     this.openPassChange = false
                 } else {
                     this.repeatError = true
                 }
            },
        }
    }
</script>

<style scoped>

</style>