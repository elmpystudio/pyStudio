<template>
    <div class="notifications">
        <div class="content">
            <div class="content-container" v-for="notification in data" :key="notification.id">
                <div class="message-container">
                    <h6 class="title">Dataset Request</h6>
                    <p class="message">{{ short_message(notification.message) }}</p>
                    <div class="more-container">
                        <p class="more">Dataset Name: Covid</p>
                        <p class="more">From User: Jameel</p>
                    </div>
                </div>
                <div class="actions-container">
                    <v-btn class="action primary" @click="handle_action('accept', notification.id)">Accept</v-btn>
                    <v-btn class="action danger" @click="handle_action('deny', notification.id)">Deny</v-btn>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "Notifications",
    props: {
        short: { type: Boolean, default: false }
    },  

    computed: {
        data(){
            return this.$store.getters.notifications;
        },
    },

    mounted() {
        this.$store.dispatch('GET_NOTIFICATIONS');
    },

    methods: { 
        handle_action(type, id) {
            if (type === 'accept') {
                this.$store.dispatch('ACCEPT_NOTIFICATION', id);
                this.$store.dispatch('GET_NOTIFICATIONS');
            }
            else if (type === 'deny') {
                this.$store.dispatch('DENY_NOTIFICATION', id);
                this.$store.dispatch('GET_NOTIFICATIONS');
            }
        },

        short_message(message){
            if(this.short)
                return message.substring(0, 60) + '...';
            return message;
        },
    }
}
</script>

<style lang="scss" scoped>
.content {
    width: 100%;
    height: 100%;
    border-radius: 3px;
    box-shadow: 0px 0px 10px rgba(138, 138, 138, 0.3490196078);
    background-color: #ffffff;
    padding: 10px;

    display: flex;
    flex-flow: column nowrap;
    row-gap: 5px;

    overflow-y: scroll;
    overflow-x: hidden;

    .content-container {
        background-color: #1976d238;
        padding: 0 20px;

        display: flex;
        flex-flow: row nowrap;
        justify-content: space-between;
        align-items: center;
        border-radius: 5px;
        column-gap: 10px;


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
                    text-align: start;
                    font-size: 11px;
                    margin: 0;
                }
            }
        }

        .actions-container {
            display: flex;
            flex-flow: row nowrap;
            column-gap: 10px;

            .action {
                width: 75px;
                font-size: 14px;
                text-transform: none;
            }
        }
    }
}
</style>
