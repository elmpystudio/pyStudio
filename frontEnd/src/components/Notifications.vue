<template>
    <div class="notifications" v-if="data.length > 0">

        <div class="content" v-for="(notification, index) in data" :key="index" :id="`notification_${index}`">
            <div class="message-container">
                <h6 class="title" v-if="notification.isRequest">
                    Request
                </h6>
                <h6 class="title" v-else>
                    Response
                </h6>
                <p class="message" v-if="notification.isRequest">{{ short_message(notification.message) }}</p>
                <p class="message" v-else>
                    Your Request is {{ acceptOrNot(notification) }}
                </p>

                <div class="more-container">

                    <div class="more">
                        <div class="name">
                            Name:
                        </div>
                        <div class="value">
                            {{ short_message(notification.name) }}
                        </div>
                    </div>

                    <div class="more">
                        <div class="name">
                            From:
                        </div>
                        <div class="value">
                            {{ notification.username }}
                        </div>
                    </div>
                </div>
            </div>
            <div class="actions-container" v-if="notification.isRequest">
                <v-btn class="action primary" @click="handle_action('accept', notification)">Accept</v-btn>
                <v-btn class="action danger" @click="handle_action('deny', notification)">Deny</v-btn>
            </div>
            <div class="actions-container" v-else>
                <v-btn class="action primary" @click="handle_ok(notification)">Ok</v-btn>
            </div>
        </div>

    </div>

    <div class="notifications empty" v-else>
        <i class="fa fa-exclamation-circle" aria-hidden="true"></i>
        There are no notifications to display
    </div>
</template>

<script>
import { datasetsAdd, ml_modelsAdd } from "@/api_client";

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
        handle_action(type, notification) {
            if (type === 'accept') {
                if (notification.type === "dataset")
                    datasetsAdd(notification.id, {
                        user_id: notification.user_id
                    })
                        .then(({ status }) => {
                            if (status === 200)
                                return;
                        })
                        .catch((error) => console.log(error))
                else
                    ml_modelsAdd(notification.id, {
                        user_id: notification.user_id
                    })
                        .then(({ status }) => {
                            if (status === 200)
                                return;
                        })
                        .catch((error) => console.log(error))
            }

            // Delete it
            this.$store.dispatch('DELETE_NOTIFICATION', notification);

            // answer
            this.$store.dispatch('SET_NOTIFICATION', {
                owner_id: notification.user_id,
                data: {
                    id: notification.id,
                    name: notification.name,
                    type: notification.type,
                    message: notification.message,
                    user_id: localStorage.getItem("user_id"),
                    username: localStorage.getItem("username"),
                    isAccept: type === 'accept'
                }
            });
        },

        handle_ok(notification) {
            if (notification.isAccept)
                location.reload();
            this.$store.dispatch('DELETE_NOTIFICATION', notification);
        },

        short_message(message) {
            if (this.short)
                if (message.length > 15)
                    return message.substring(0, 30) + '...';
            return message;
        },

        acceptOrNot(notification) {
            if (notification.isAccept)
                return 'Aceepted';
            return 'Denied';
        }
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
