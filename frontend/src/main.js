import {createApp} from 'vue';
import {createRouter, createWebHashHistory} from 'vue-router';

import App from './App.vue';
import AnalysisListing from './views/AnalysisListing.vue';
import AnalysisCreate from './views/AnalysisCreate.vue';
import About from './views/About.vue';

import './styles/main.css';
// import './styles/proxima-nova-font.css'

const routes = [
  {path: '/', component: AnalysisListing},
  {path: '/analysis/create', component: AnalysisCreate},
  {path: '/about', component: About},
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

createApp(App)
    .use(router)
    .mount('#app');
