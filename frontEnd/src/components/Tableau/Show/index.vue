<template>
  <div>
    <div ref="tableau"></div>
  </div>
</template>

<script>
  export default {
    name: "Show",
    data() {
      return {
        url: `http://35.208.41.132:8999/trusted/${localStorage.getItem('key')}/t/API/views/${this.$route.params.name}/Sheet1`,
        options: {
          hideTabs: true,
          height: '100vh',
          width: '100%',
        },
        workbooks: [],
      }
    },
    methods: {
      initViz: function () {
        new window.tableau.Viz(this.$refs.tableau, this.url, this.options);
      }
    },
    mounted: function () {
      this.initViz();
    }
  }
</script>

<style scoped>

</style>
