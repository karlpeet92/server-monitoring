<template>
  <v-simple-table fixed-header dense height="350px">
    <template v-slot:default>
      <thead>
          <tr>
            <th class="text-left">Time of Request</th>
            <th class="text-left">Request Time</th>
            <th class="text-left">Status</th>
          </tr>
      </thead>
      <tbody>
        <tr v-for="item in tableData" :key="item.time">
          <td>{{ item.time }}</td>
          <td>{{ item.response_time}}</td>
          <td>{{ item.response_code }}</td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
</template>

<script>
    export default {
        name: "conn-table-row",
        components: {},
        props: ['tableData'],
        data() {
            return {}
        },
        mounted() {
        },
    }
</script>

<style scoped>

</style>