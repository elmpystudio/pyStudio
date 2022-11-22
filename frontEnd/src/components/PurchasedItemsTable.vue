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
          { text: 'Purchase Date', value: 'purchaseDate' },
          { text: 'Expiration Date', value: 'expiraitonDate' },
          { text: 'Quota', value: 'quota' },
          { text: 'Consumption', value: 'consumption' },
        ],
        projects: [
          {
            name: 'Report sales 2019',
            type: 'Report',
            purchaseDate: '12.04.2019 10:30',
            expiraitonDate: '15.05.2020 10:30',
            quota: 1000,
            consumption: 'None',
          },
          {
            name: 'Car Sales 2000 - 2019',
            type: 'Service',
            purchaseDate: '12.04.2019 10:30',
            expiraitonDate: '15.05.2020 10:30',
            quota: 4000,
            consumption: 'None',
          },
        ]
      }
    }
  }
</script>

<style scoped lang="scss">

</style>