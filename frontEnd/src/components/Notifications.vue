<template>
    <div class="notifications" v-if="data.length > 0">
        <div class="content" v-for="notification in data" :key="notification.id" :id="`notification_${notification.id}`">
            <div class="message-container">
                <h6 class="title">Dataset Request</h6>
                <p class="message">{{ short_message(notification.message) }}</p>
                <div class="more-container">
                    <div class="more">
                        <div class="name">
                            Dataset:
                        </div>
                        <div class="value">
                            {{ notification.dataset.name }}
                        </div>
                    </div>

                    <div class="more">
                        <div class="name">
                            From:
                        </div>
                        <div class="value">
                            {{ notification.from_user.username }}
                        </div>
                    </div>
                </div>
            </div>
            <div class="actions-container">
                <v-btn class="action primary" @click="handle_action('accept', notification.id)">Accept</v-btn>
                <v-btn class="action danger" @click="handle_action('deny', notification.id)">Deny</v-btn>
            </div>
        </div>
    </div>

    <div class="notifications empty" v-else>
        <i class="fa fa-exclamation-circle" aria-hidden="true"></i>
        There are no notifications to display
    </div>
</template>

<script>
import $ from 'jquery';

export default {
    name: "Notifications",
    props: {
        short: { type: Boolean, default: false }
    },

    computed: {
        data() {
            return this.$store.getters.notifications;
        },
    },

    methods: {
        handle_action(type, id) {
            if (type === 'accept')
                this.$store.dispatch('ACCEPT_NOTIFICATION', id);
            else if (type === 'deny')
                this.$store.dispatch('DENY_NOTIFICATION', id); 

            $(`#notification_${id}`).addClass("hide");
            this.$store.dispatch('GET_NOTIFICATIONS');
        },

        short_message(message) {
            if (this.short)
                return message.substring(0, 60) + '...';
            return message;
        },
    }
}
</script>

<style lang="scss" scoped>
.notifications {
    width: 100%;
    height: 100%;
    padding: 10px;

    overflow-y: scroll;
    overflow-x: hidden;

    display: flex;
    flex-flow: column nowrap;
    row-gap: 5px; 

    /* width */
    &::-webkit-scrollbar {
        width: 5px;
    }

    /* Track */
    &::-webkit-scrollbar-track {
        background: #f1f1f1;
    }

    /* Handle */
    &::-webkit-scrollbar-thumb {
        background: #888;

        &:hover {
            background: #555;
        }
    }

    .content {
        background-color: #e7e7e7;
        padding: 0 20px;

        display: flex;
        flex-flow: row nowrap;
        justify-content: space-between;
        align-items: center;
        border-radius: 5px;
        column-gap: 10px;
        

        &.hide {
            display: none;
        }

        .message-container {
            height: 120px;
            padding: 5px 0;
            display: flex;
            flex-flow: column nowrap;
            justify-content: space-between;


            .title {
                text-align: start;
                font-size: 18px !important;
                margin: 0;
            }

            .message {
                text-align: start;
                font-size: 15px;
                margin: 0;
            }

            .more-container {
                .more {
                    display: flex;
                    flex-flow: row nowrap;
                    column-gap: 5px;

                    .name {
                        font-size: 11px;
                        font-weight: bold;
                    }

                    .value {
                        font-size: 11px;
                    }
                }
            }
        }

        .actions-container {
            display: flex;
            flex-flow: row nowrap;
            column-gap: 10px;

            .action {
                width: 70px;
                font-size: 14px;
                text-transform: none;
            }
        }
    }

    &.empty {
        >i {
            font-size: 30px;
            color: grey;
        }
    }
}
</style>
