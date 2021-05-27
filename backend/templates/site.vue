<template id='vueapp'>


    <div >
        <ol>
            <li>ID:</li>
            <li>email:</li>
            <button id="site_button" onclick= "openSite()">user site</button>
        </ol>
    </div>

</template>

<script>
    export default {
        name:"user",
        data() {
            return {
                id: null,
                name: null,
                url: null
            }
        }
    }
</script>