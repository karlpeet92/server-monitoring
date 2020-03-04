<template>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>

    <link rel="stylesheet" type="text/css" href="">
    <title>Document</title>
</head>
<body id='vueapp'>
    <div inline-template>        
        <ol>           
            <li>ID: {{user.id}} </li>          
            <li>email: {{user.email}}</li>
            <li>first name: {{user.first_name}}</li>
            <li>last name: {{user.last_name}}</li>
            <li>phone nr: {{user.phone_number}}</li>
            <button id="site_button" onclick= "openSite()">user site</button>            
        </ol>
    </div>
</body>
</template>

<script>

    import axios from 'axios';

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
function openSite(){
    document.getElementById("site_button").addEventListener('click', getJSON())
}

function getJSON() {
    let response = axios.get('http://server-monitor.dev.codecloud.ee:9001/api/user-site/', {
        params: {
            user_id: '{{user.id}}'
        }        
    })
    .then((response) => {
    if (response) {
        console.log(response);
        this.id = data.result.id;
        this.name = data.result.name;
        this.url = data.result.url
        }
    })
}


</script>
