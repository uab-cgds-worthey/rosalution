import {createApp} from 'vue';
import {createRouter, createWebHashHistory} from 'vue-router';

import App from './App.vue';
import AnalysisListingView from './views/AnalysisListingView.vue';
import AnalysisCreateView from './views/AnalysisCreateView.vue';
import AboutView from './views/AboutView.vue';

import './styles/main.css';
// import './styles/proxima-nova-font.css'

import {library} from '@fortawesome/fontawesome-svg-core';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import {
  faUser, faUsers, faUserGroup, faCalendar, faBookOpen, faList, faLayerGroup,
  faBoxArchive, faQuestion, faClock, faClipboardCheck}
  from '@fortawesome/free-solid-svg-icons';

library.add(
    faUser, faUsers, faUserGroup, faCalendar, faBookOpen, faList,
    faLayerGroup, faBoxArchive, faQuestion, faClock, faClipboardCheck);

const routes = [
  {path: '/', component: AnalysisListingView},
  {path: '/analysis/create', component: AnalysisCreateView},
  {path: '/about', component: AboutView},
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

const app = createApp(App);

app.use(router);
app.component('font-awesome-icon', FontAwesomeIcon);
app.mount('#app');
