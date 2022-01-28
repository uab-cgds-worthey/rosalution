import {createApp} from 'vue';
import {createRouter, createWebHashHistory} from 'vue-router';

import App from './App.vue';
import AnalysisListingView from './views/AnalysisListingView.vue';
import AnalysisCreateView from './views/AnalysisCreateView.vue';
import AboutView from './views/AboutView.vue';

import './styles/main.css';
// import './styles/proxima-nova-font.css'

const routes = [
  {path: '/', component: AnalysisListingView},
  {path: '/analysis/create', component: AnalysisCreateView},
  {path: '/about', component: AboutView},
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

createApp(App)
    .use(router)
    .mount('#app');
