<template>
    <div class="content">
        <Dashboard />
    </div>
</template>

<script>
import Dashboard from '@/components/Dashboard';

export default {
    name: 'DashboardView',
    components: {
        Dashboard
    }
};
</script>

<style scoped lang="scss">
.content {
    height: 100%;
}
</style>
