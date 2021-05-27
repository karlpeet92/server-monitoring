<template>
    <v-layout style="height:0; margin-top:175px; z-index: 1" row justify-center v-if="index === null || index === 0">
        <v-dialog v-model="dialog" @keydown.esc="dialog=false" @keydown.enter="registerData()" persistent max-width="600px">
            <template v-slot:activator="{ on }">
                <v-btn color="primary" dark v-on="on">Add User</v-btn>
            </template>
            <v-card>
                <v-card-title>
                    <span class="headline">User profile</span>
                </v-card-title>
                    <v-card-text>
                        <v-container>
                            <v-row>
                                <v-col cols="12" sm="6" md="6">
                                    <v-text-field :rules="nameRules" label="First name*" v-model="first_name" required></v-text-field>
                                </v-col>

                                <v-col cols="12" sm="6" md="6">
                                    <v-text-field
                                        :rules="nameRules"
                                        label="Last name*"
                                        v-model="last_name"
                                        required
                                    ></v-text-field>
                                </v-col>
                                <v-col cols="12">
                                    <v-text-field :rules="emailRules" label="Email*" v-model="email" required></v-text-field>
                                </v-col>
                                <v-col cols="12">
                                    <v-text-field :rules="passwordRules" label="Password*" v-model="password" type="password" required></v-text-field>
                                </v-col>
                                <v-col cols="12">
                                    <v-text-field label="Confirm Password*" v-model="confirm_password" type="password" required></v-text-field>
                                </v-col>
                            </v-row>
                        </v-container>
                        <small>*indicates required field</small>
                    </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="closeRegDialog()">Close</v-btn>
                    <v-btn color="blue darken-1" text @click="registerData()">Add User</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-layout>
</template>

<script>
    import {mapActions, mapState} from "vuex";

    export default {
        name: "UserRegForm",
        data: () => ({
            dialog: false,
            first_name:"",
            last_name: "",
            nameRules: [
                v => !!v || 'Name is required',
            ],
            email: "",
            emailRules: [
                v => !!v || 'E-mail is required',
                v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
            ],
            password:"",
            passwordRules: [
                value => (value.length >=7) || 'Min 7 characters'
            ],
            confirm_password:"",
        }),
        mounted() {

        },
        computed:{
            ...mapState(["index", "userID"])
        },
        methods: {
            async closeRegDialog() {
                this.dialog = false;
                this.first_name = "";
                this.last_name = "";
                this.email = "";
                this.password = "";
                this.confirm_password = "";
            },
            ...mapActions(["register"]),
            async registerData () {
                if(this.valid()) {
                    await this.$store.dispatch("register", {
                              form: "registration",
                        first_name: this.first_name,
                         last_name: this.last_name,
                             email: this.email,
                          password: this.password,
                    });
                    this.dialog = false
                }
            },
            valid () {
                return this.password === this.confirm_password && this.password.length >= 7 ;
            },
        }
    }
</script>

<style scoped>

</style>