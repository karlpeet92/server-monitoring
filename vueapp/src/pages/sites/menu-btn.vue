<template>
    <div class="text-center" v-if="index === 1">
        <v-menu offset-y auto>
          <template v-slot:activator="{ on, attrs }">
            <v-app-bar-nav-icon
              class="menu-btn"
              v-bind="attrs"
              v-on="on"
            >
            </v-app-bar-nav-icon>
          </template>
          <v-list>
            <v-list-item
              v-for="(item, index) in items"
              :key="index"
              @click="item.action"
            >
              <v-list-item-title >{{ item.title }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>

        <pass-repeat v-if="pass_repeat" :showPassRepeat="pass_repeat"
                     @close="pass_repeat = false" @notify="[pass_repeat = false, pass_change = true]" />
        <pass-change v-if="pass_change" :showPassChange="pass_change" @close="pass_change = false" />
    </div>
</template>

<script>
    import {mapActions, mapState} from 'vuex';
    import PassRepeat             from "./pass-repeat";
    import PassChange             from "./pass-change";

    export default {
        name: "menu-btn",
        components: {PassRepeat, PassChange},
        data () {
            return{
              pass_repeat: false,
              pass_change: false,
              items: [
                { title: 'sign out',
                  action: this.logout,
                },
                { title: 'Change password',
                  action: this.pass,
                }
              ],
            }
        },
        computed: {
            ...mapState(['index'])
        },
        methods: {
            logout() {
                this.$store.commit('logoutIdx', {
                    idx: 0
                });
            },
            pass() {
                this.pass_repeat = true;
            }
        }
    }

</script>

<style scoped>

</style>