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
        headers: [
          { text: 'Name', value: 'name' },
          { text: 'Type', value: 'type' },
          { text: 'Publish Date', value: 'publishDate' },
        ],
        projects: [
          {
            name: 'Report sales 2019',
            type: 'Report',
            publishDate: '12.04.2019 10:30',
          },
          {
            name: 'New York City_Sales.csv',
            type: 'Dataset',
            publishDate: '12.04.2019 10:45',
          },
        ]
      }
    }
  }
</script>

<style scoped lang="scss">

</style>