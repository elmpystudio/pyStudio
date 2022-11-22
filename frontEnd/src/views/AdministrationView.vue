<template>
    <div class="content">
        <Administration
            :url="url"
        />
    </div>
</template>

<script>
import Administration from '@/components/Administration';

export default {
    name: 'AdministrationView',
    components: {
        Administration
    },

    data: () => ({
        url: "http://localhost:8000/api/admin",
    }),
}
</script>

<style scoped lang="scss">
.content {
    width: 100%;
    height: 100%;
    padding: 5px
}
</style>
