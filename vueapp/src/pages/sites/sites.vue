<template>
    <div>
        Olen Template: {{message}}
        <br />
        <a href="javascript: {}" @click="changeMessage()">Test me</a>
    </div>
</template>
<script>
    import {mapActions, mapState} from "vuex";

    export default {
        data() {
            return {}
        },
        mounted() {

        },
        computed: {
            ...mapState(['message'])
        },
        methods: {
            ...mapActions(['getSites']),
            changeMessage() {
                this.getSites()
            }
        }
    }
</script>