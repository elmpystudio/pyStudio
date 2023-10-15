import Vue from 'vue';
import Vuex from 'vuex';
import db from '@/firebase'
import { onSnapshot, doc, setDoc, arrayUnion, arrayRemove, } from "firebase/firestore";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        notifications: []
    },
    mutations: {
        // 
    },
    actions: {
        GET_NOTIFICATIONS({ state }) {
            onSnapshot(doc(db, "notifications", localStorage.getItem("user_id")), (doc) => {
                if(doc.data())
                    state.notifications = doc.data().data;
            });
        },

        async SET_NOTIFICATION(NULL, payload) {
            console.log("STORE, ", payload)
            await setDoc(doc(db, "notifications", payload.owner_id+""), {
                data: arrayUnion(payload.data)
            }, { merge: true });
        },

        async DELETE_NOTIFICATION({ commit }, payload) {
            commit;
            await setDoc(doc(db, "notifications", localStorage.getItem("user_id")), {
                data: arrayRemove(payload)
            }, { merge: true });
        },

    },
    getters: {
        notifications(state) {
            return state.notifications;
        }
    }
})
