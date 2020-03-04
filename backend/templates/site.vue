<template>
    <body>
    <div>
        <ol>
            <li>site ID: {{id}},</li>
            <li>name: {{name}},</li>
            <li>URL: {{url}}</li>
        </ol>            
    </div>
</body>
</template>

<script>
    export default {
        name:"Site",

        data() {
            return {
                id: null,
                name: null,
                URL: null
            }
        },
        methods: {
        }
    }
</script>