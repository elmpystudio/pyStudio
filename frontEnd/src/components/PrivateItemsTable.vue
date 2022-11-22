<template>
    <v-data-table
    :headers="headers"
    :items="projects"
    :hide-default-footer="true"
    :search="sort"
    item-value="value"
    item-text="label"
    class="elevation-1"
  ></v-data-table>
</template>

<script>
  export default {
    name: "ItemsTable",
    props: ['sort'],
    data() {
      return {
        search: '',
        headers: [
          { text: 'Name', value: 'name' },
          { text: 'Format', value: 'format' },
          { text: 'Type', value: 'type' },
          { text: 'Last Updated', value: 'updatedAt' },
        ],
        projects: [
          {
            name: 'Report sales 2019',
            format: 'PDF',
            type: 'Report',
            updatedAt: '12.04.2019 10:30',
          },
          {
            name: 'New York City_Sales.csv',
            format: 'CSV',
            type: 'Dataset',
            updatedAt: '12.04.2019 10:45',
          },
        ]
      }
    }
  }
</script>

<style scoped lang="scss">

</style>