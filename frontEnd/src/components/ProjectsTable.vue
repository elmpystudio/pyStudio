<template>
    <v-data-table
    :headers="headers"
    :items="projects"
    :hide-default-footer="true"
    class="elevation-1"
  ></v-data-table>
</template>

<script>
  export default {
    name: "ProjectsTable",
    data() {
      return {
        headers: [
          { text: 'Name', value: 'name' },
          { text: 'Last updated', value: 'updatedAt' },
          { text: 'Owner', sortable: false, value: 'owner' },
          { text: 'Team', sortable: false, value: 'team' },
        ],
        projects: [
          {
            name: 'Car Price Predictor',
            updatedAt: '12.04.2019, 14:00',
            owner: 'Me',
            team: 4.0,
          },
          {
            name: 'NY Apartments Prices Predictor',
            updatedAt: '12.04.2019, 14:00',
            owner: 'John Smith',
            team: 4.0,
          },
        ]
      }
    }
  }
</script>

<style scoped lang="scss">

</style>