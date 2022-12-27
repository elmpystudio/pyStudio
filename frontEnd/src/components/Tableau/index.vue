<template>
  <div class="content">
    <v-row>
      <v-col lg="3" md="4" sm="6" xs="6" :key="workbook.id" v-for="workbook in workbooks">
        <v-card
          class="tableau-card"
        >
          <v-img
            class="white--text align-end"
            height="200px"
            src="@/assets/data.jpg"
          >
            <v-card-title class="font-weight-bold">{{ workbook.name }}</v-card-title>
          </v-img>

          <v-card-text class="text--primary">
            <div>Dataset description dataset description</div>
          </v-card-text>

          <v-card-actions>
            <v-btn
              :to="{ name: 'analytics-view', params: { name: workbook.name }}"
              text
              color="#2f6bff"
            >
              View
            </v-btn>

            <v-btn
              :to="{ name: 'analytics-edit', params: { name: workbook.name }}"
              text
              color="#2f6bff"
            >
              Edit
            </v-btn>

            <v-btn
              :to="{ name: 'analytics-publish', params: { id: workbook.id }}"
              text
              color="#2f6bff"
            >
              Publish
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
  // import { getTableauToken, getWorkbooks, getMyIP } from '@/api_client.js';
  export default {
    name: "Tableau",
    data() {
      return {
        workbooks: [],
      }
    },
    // mounted: function () {
    //   getMyIP()
    //     .then(response => {
    //       getTableauToken(response.data)
    //         .then(({ status, data }) => {
    //           if (status === 200) {
    //             data.key && localStorage.setItem('key', data.key);
    //           }
    //         });
    //     })
    //     .catch(error => console.error(error));
    //   getWorkbooks()
    //     .then(({ data }) => {
    //       this.workbooks = data.workbooks || [];
    //     });
    // }
  }
</script>

<style scoped lang="scss">
  .content {
    width: 100%;
    height: 100%;
    background-color: #f4f6fa;
    padding: 30px;

    .tableau-card {
    }
  }
</style>
