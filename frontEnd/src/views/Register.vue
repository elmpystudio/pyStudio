<template>
  <div class="register-view">
    <Register />
  </div>
</template>

<script>
  import Register from '@/components/Register';

  export default {
    name: "RegisterView",
    components: {
      Register,
    },
  }
</script>

<style scoped lang="scss">
  .register-view {
    min-height: 100vh;
    width: 100%;
    display: flex;
    background-color: #f3f3f3;
  }
</style>