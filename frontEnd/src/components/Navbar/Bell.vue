<template>
    <div>
        <v-menu offset-y :close-on-content-click="false">
            <template v-slot:activator="{ on, attrs }">
                <div v-bind="attrs" v-on="on">
                    <v-badge :content="$store.getters.notifications.length.toString()" color="red" overlap>
                        <v-icon size="29">mdi-bell-outline</v-icon>
                    </v-badge>
                </div>
            </template>

            <div class="bell-container">

                <div class="header">
                    Notifications
                </div>

                <div class="notifications-container">
                    <Notifications short />
                </div>

                <router-link class="link" :to="{ name: 'notifications' }">
                    All Notifications
                </router-link>
            </div>
        </v-menu>
    </div>
</template>

<script>
import Notifications from '@/components/Notifications.vue';

export default {
    name: "Bell",
    components: {
        Notifications
    },

    data() {
        return {

        }
    },

    mounted() {
        this.$store.dispatch('GET_NOTIFICATIONS');
    }
}
</script>

<style scoped lang="scss">
.bell-container {
    width: 500px;
    height: 500px;
    display: flex;
    background-color: #FFFFFF;
    flex-flow: column nowrap;
    justify-content: space-between;

    .header {
        background-color: #F2F2F2;
        padding: 5px;
        font-size: 20px;
    }

    .notifications-container {
        flex: 1 1 100%;
        overflow: hidden;
    }

    .link {
        background-color: #F2F2F2;
        flex: 1 1 30px;
        padding: 5px;
        cursor: pointer;
        color: #2B468B;
    }
}
</style>
