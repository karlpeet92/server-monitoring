<template>
    <v-layout style="height:500px; z-index: 1" row justify-center v-if="index === null || index === 0">
        <v-dialog v-model="dialog" @keydown.esc="dialog=false" @keydown.enter="userLogin()" max-width="600px">
            <template v-slot:activator="{ on }">
                <v-btn id="login-btn" color="primary" dark v-on="on">Login</v-btn>
            </template>
            <v-card>
                <v-card-title>
                    <span class="headline">Login</span>
                </v-card-title>
                    <v-card-text>
                        <v-container>
                            <v-row>
                                <v-col cols="12">
                                    <v-text-field hide-details id="log-email" label="Email*" v-model="email" required></v-text-field>
                                    <span style="color: red" v-if="emailPass === false">Email does not exist</span>
                                </v-col>
                                <v-col cols="12">
                                    <v-text-field id="log-pass" label="Password*" v-model="password" type="password" required></v-text-field>
                                    <span style="color: red" v-if="pass === false ">This password is invalid</span>
                                </v-col>
                            </v-row>
                        </v-container>
                        <small>*indicates required field</small>
                    </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn id="form-close-btn" color="blue darken-1" text @click="closeDialog()">Close</v-btn>
                    <v-btn id="form-login-btn" color="blue darken-1" text @click="userLogin()">Login</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-layout>
</template>

<script>
    import {mapActions, mapState} from "vuex";

  export default {
      name: "LoginForm",
      props: {
      },
      data() {
          return {
              dialog: false,
              email: "",
              password: "",
          }
      },
      mounted() {

      },
      computed: {
          ...mapState(["index", "emailPass", "pass"])
      },
      methods: {
          closeDialog() {
              this.dialog = false;
              this.email = "";
              this.password = "";
              this.$store.commit('pass', {
                 pass: true
              });
              this.$store.commit('passEmail', {
                  emailPass: true
              })
          },
          ...mapActions(["getSites"]),
          async userLogin () {
              await this.$store.dispatch("login",{
                  form: "login",
                  email: this.email,
                  password: this.password,
              });
              if(this.index === 1) {
                await this.getSites();
              }
              if(this.pass === true) {
                  this.dialog = false;
                  this.email = "";
                  this.password = "";
              }
          }
      },
  }
</script>