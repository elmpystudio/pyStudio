<template>
  <div class="notifications">
    <div class="content">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        :class="[notification.active ? 'active' : '', 'notification']"
      >
        <div>
          <p class="description">{{ notification.description }}</p>
          <span class="time">{{ notification.time }}</span>
        </div>
        <span
          @click="handleReadNotification(notification.id)"
          v-if="notification.active"
          class="mark-text"
        >
          Mark as read
        </span>
      </div>
    </div>
  </div>
</template>

<script>
  import vClickOutside from 'v-click-outside';
  import { mapState, mapGetters } from 'vuex';

  export default {
    name: "Notifications",
    directives: {
      clickOutside: vClickOutside.directive,
    },
    components: {
    },

    computed: {
      ...mapGetters(['totalActiveNotifications']),
      ...mapState(['notifications']),
    },
    methods: {
      handleReadNotification(id) {
        this.$store.dispatch('readNotification', id);
      }
    }
  }
</script>

<style lang="scss" scoped>
  .content {
    padding: 30px;

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
      }

      .time {
        color: #9296ad;
        font-size: 16px;
        font-weight: 500;
      }
    }
  }
</style>
