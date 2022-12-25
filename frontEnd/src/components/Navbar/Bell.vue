<template>
    <div>
        <v-menu offset-y>
            <template v-slot:activator="{ on, attrs }">
                <div v-bind="attrs" v-on="on">
                    <v-badge :content="$store.getters.notifications.length.toString()" color="red" overlap>
                        <v-icon size="29">mdi-bell-outline</v-icon>
                    </v-badge>
                </div>
            </template>

            <div class="notifications">
                <Notifications short />

                <router-link class="go_to" :to="{ name: 'notifications' }">
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
    }
}
</script>

<style scoped lang="scss">
.notifications {
    width: 500px;
    height: 500px;
    display: flex;
    flex-flow: column nowrap;
    justify-content: space-between;


    .go_to {
        flex: 1 1 100%;
        padding: 5px;
        cursor: pointer;
        background-color: #CEDFEF;
        transition: all 300ms;
        opacity: 1;

        &:hover {
            opacity: 0.9;
        }

    }
}
</style>
