<template>
    <div class="notifications-view">
        <Notifications />
    </div>
</template>

<script>
import Notifications from '@/components/Notifications.vue';

export default {
    name: "NotificationsView",
    components: {
        Notifications,
    }
}
</script>

<style scoped lang="scss">
.notifications-view {
    padding: 30px
}
</style>
