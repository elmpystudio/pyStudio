<template>
  <v-data-table
    :headers="headers"
    :items="items"
    :hide-default-footer="true"
    class="elevation-1"
  ></v-data-table>
</template>

<script>
  export default {
    name: "DataSampleTable",
    data() {
      return {
        headers: [
          { text: 'Age', value: 'age' },
          { text: 'Job', value: 'job' },
          { text: 'Marital', value: 'marital' },
          { text: 'Education', value: 'education' },
          { text: 'Loan', value: 'loan' },
          { text: 'Housing', value: 'housing' },
          { text: 'Day', value: 'day' },
          { text: 'Month', value: 'month' },
        ],
        items: [
          {
            age: '65',
            job: 'management',
            marital: 'married',
            education: 'university',
            loan: 0,
            housing: 1,
            day: 5,
            month: 'may',
          },
          {
            age: '65',
            job: 'management',
            marital: 'married',
            education: 'university',
            loan: 0,
            housing: 1,
            day: 5,
            month: 'may',
          },
          {
            age: '65',
            job: 'management',
            marital: 'married',
            education: 'university',
            loan: 0,
            housing: 1,
            day: 5,
            month: 'may',
          },
          {
            age: '65',
            job: 'management',
            marital: 'married',
            education: 'university',
            loan: 0,
            housing: 1,
            day: 5,
            month: 'may',
          },
          {
            age: '65',
            job: 'management',
            marital: 'married',
            education: 'university',
            loan: 0,
            housing: 1,
            day: 5,
            month: 'may',
          },
        ]
      }
    }
  }
</script>

<style scoped lang="scss">

</style>
