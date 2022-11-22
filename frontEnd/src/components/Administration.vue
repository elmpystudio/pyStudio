<template>
    <div class="conetnt">
        <iframe :src="url" frameBorder="0" width="100%" height="100%" />
    </div>
</template>

<script>
export default {
    props: {
        url: { type: String, required: true },
    }
}
</script>

<style lang="scss" scoped>
.conetnt {
    width: 100%;
    height: 100%;
}
</style>