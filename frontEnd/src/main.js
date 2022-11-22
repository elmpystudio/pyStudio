import Vue from 'vue';
import Vuelidate from 'vuelidate'
import App from './App.vue';
import vuetify from './plugins/vuetify';
import router from './router';
import store from './store';
import 'bootstrap' 

Vue.config.productionTip = false;
Vue.use(Vuelidate);

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
