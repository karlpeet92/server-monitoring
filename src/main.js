import Vue       from 'vue';

import Home      from '../backend/templates/home.vue';
import User      from '../backend/templates/user.vue';
import Site      from '../backend/templates/site.vue';

 
let vueapp = new Vue({
    el: '#vueapp',
    components: {
        'home' : Home,
        'user' : User,
        'site' : Site,
    }
})