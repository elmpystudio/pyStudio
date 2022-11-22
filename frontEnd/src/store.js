import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    user: { id: 1234, name: 'Test User' },
    notifications: [
      {
        id: 1,
        description: 'Dataset Car Prices in Western Europe has been updated to new version.',
        time: '3h ago',
        active: true,
      },
      {
        id: 2,
        description: 'Someone sent you request for publishing item on the marketplace.',
        time: '4h ago',
        active: true,
      },
      {
        id: 3,
        description: 'John added you to the project Car category',
        time: '5h ago',
        active: false,
      },
    ],
  },
  mutations: {
    READ_NOTIFICATION(state, id) {
      const notification = state.notifications.find(item => item.id === id);
      if (typeof notification !== 'undefined') {
        notification.active = false;
      }
    }
  },
  actions: {
    readNotification({ commit }, id) {
      commit('READ_NOTIFICATION', id);
    }
  },
  getters: {
    totalActiveNotifications: state => state.notifications.filter(item => item.active).length,
    notificationsPreview: state => state.notifications.slice(0, 10),
  }
})
