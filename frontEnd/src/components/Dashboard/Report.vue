<template>
  <div>
    <div class="d-flex align-center justify-center loader-container" v-if="isLoading">
      <v-progress-circular
        :size="50"
        color="primary"
        indeterminate
      ></v-progress-circular>
    </div>
    <template v-else>
      <iframe class="report" :srcdoc="raport"></iframe>
    </template>
  </div>
</template>

<script>
  import { getHTMLRaport } from '@/api_client.js';

  export default {
    name: "Report",
    data() {
      return {
        raport: '',
        isLoading: false,
      }
    },
    created() {
      this.isLoading = true;
      getHTMLRaport(this.$route.params.id)
        .then(({ data }) => {
          this.isLoading = false;
          this.raport = data.raport;
        })
        .catch((error) => {
          console.error(error);
          this.isLoading = false;
        })
    }
  }
</script>

<style scoped>
  .loader-container {
    min-height: 350px;
  }

  .report {
    border: none;
    width: 100%;
    min-height: 100vh;
  }
</style>
