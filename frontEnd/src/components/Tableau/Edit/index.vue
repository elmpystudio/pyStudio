<template>
  <div ref="tableau"></div>
</template>

<script>
  export default {
    name: "Edit",
    data() {
      return {
        url: `http://35.208.41.132:8999/trusted/${localStorage.getItem('key')}/t/API/authoring/${this.$route.params.name}/Sheet1`,
        options: {
          hideTabs: false,
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
