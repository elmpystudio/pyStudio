<template>
    <div>
        <v-menu offset-y>
            <template v-slot:activator="{ on, attrs }">
                <div v-bind="attrs" v-on="on" >
                    <v-badge 
                    :content="totalActiveNotifications"
                    :value="totalActiveNotifications"
                    color="red"
                    overlap>
                        <v-icon size="29">mdi-bell-outline</v-icon>
                    </v-badge>
                </div>
            </template>
            
            <div class="notifications">
                <div style="height: 100%;" class="content d-flex flex-column justify-content-between">
                    <div
                    v-for="notification in notificationsPreview"
                    :key="notification.id"
                    :class="[notification.active ? 'active' : '', 'notification']"
                    @click="handleReadNotification(notification.id)">
                        <p class="description">{{ notification.description }}</p>
                        <span class="time">{{ notification.time }}</span>
                    </div>

                    <router-link :to="{ name: 'notifications'}" tag="div" class="notifications-link">
                        All notifications
                    </router-link>
                </div>
            </div>
        </v-menu>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    name: "Notifications",
    
    methods: {
        handleReadNotification(id) {
            this.$store.dispatch('readNotification', id);
        },
    },
    computed: {
        ...mapGetters(['notificationsPreview', 'totalActiveNotifications']),
    }
}
</script>

<style scoped lang="scss">
.v-menu__content {
    overflow: hidden;
}

.notifications {
    width: 500px;
    height: 300px;
    padding: 2px;
    background: white;

    .content {
      min-width: 500px;
      border-radius: 3px;
      box-shadow: 0px 0px 10px rgba(138, 138, 138, 0.3490196078);
      background-color: #ffffff;
      color: #0a1448;
      position: absolute;
      right: 0;
      z-index: 1;
      padding: 10px;

      .notification {
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
        padding: 10px;
        box-shadow: 0 13px 12px 0 #eaedf4;
        background-color: #ffffff;

        &.active {
          background-color: rgba(0, 114, 255, 0.2);
        }

        .mark-text {
          font-size: 12px;
          font-weight: bold;
          cursor: pointer;
        }

        .description {
          margin: 0;
          display: flex;
          flex: 4;
        }

        .time {
          display: flex;
          flex: 1;
          justify-content: flex-end;
          color: #9296ad;
          font-size: 16px;
          font-weight: 500;
        }
      }

      .notifications-link {
        padding: 6px 0;
        display: flex;
        justify-content: center;
        font-weight: bold;
      }

      .notifications-link:hover {
          cursor: pointer;
      }
    }
}
</style>
