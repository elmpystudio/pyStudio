import Vue from 'vue';
import Vuex from 'vuex';
import { getNotifications, acceptNotification, denyNotification } from '@/api_client.js';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        notifications: [],
    },
    mutations: {
        // 
    },
    actions: {
        GET_NOTIFICATIONS({ state }) {
            getNotifications()
                .then(({ data }) => {
                    state.notifications = data;
                })
                .catch((error) => console.log(error))
        },
        ACCEPT_NOTIFICATION({state}, id) {
            acceptNotification(id)
                .then(() => {
                    console.log(state)

                })
                .catch((error) => console.log(error))
        },
        DENY_NOTIFICATION({state}, id) {
            denyNotification(id)
                .then(() => {
                    console.log(state)
                })
                .catch((error) => console.log(error))
        },

    },
    getters: {
        notifications(state) {
            return state.notifications;
        }
    }
})
