<template>
    <v-layout row justify-center>
        <v-dialog v-model="showPassRepeat"
                  @click:outside="$emit('close')"
                  @keydown.esc="$emit('close')"
                  @keydown.enter="[passRepeat(), $emit('notify')]"
                  max-width="600px">
            <v-card>
                <v-card-title class="headline">Please enter your current password</v-card-title>
                <v-card-text>
                    <v-container>
                        <v-row>
                            <v-col cols="12">
                                <v-text-field hide-details type="password" label="Current password" v-model="current_password"></v-text-field>
                                <span style="color: red" v-if="checkPass === false">Wrong password</span>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
                <v-card-actions>
                    <v-btn color="blue darken-1" text @click="$emit('close')">Cancel</v-btn>
                    <v-btn color="blue darken-1" text @click="[passRepeat(), $emit('notify')]">Next</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-layout>
</template>

<script>
    import { mapState, mapActions} from 'vuex'

    export default {
        name: "pass-repeat",
        props: ["showPassRepeat"],
        data() {
            return {
                current_password: "",
            }
        },
        mounted() {
        },
        computed: {
            ...mapState(["userEmail", "checkPass"])
        },
        methods: {
            ...mapActions([""]),
            async passRepeat () {
                await this.$store.dispatch("passCheck", {
                    form: "password-check",
                    email: this.userEmail,
                    password: this.current_password
                });
            }
        }
    }
</script>

<style scoped>

</style>