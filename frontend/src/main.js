import {createApp} from 'vue';
import {createRouter, createWebHistory} from 'vue-router';

import App from './App.vue';
import AnalysisListingView from './views/AnalysisListingView.vue';
import AnalysisCreateView from './views/AnalysisCreateView.vue';
import AboutView from './views/AboutView.vue';
import NotFoundView from './views/NotFound.vue';
import AnalysisView from './views/AnalysisView.vue';

import './styles/main.css';
// import './styles/proxima-nova-font.css'

import {library} from '@fortawesome/fontawesome-svg-core';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import {
  faAsterisk, faPause, faCheck, faX, faUser, faUsers, faUserGroup, faCalendar, faBookOpen, faList, faLayerGroup,
  faBoxArchive, faQuestion, faClock, faClipboardCheck, faMagnifyingGlass} from '@fortawesome/free-solid-svg-icons';

library.add(
    faAsterisk, faPause, faCheck, faX, faMagnifyingGlass, faUser, faUsers, faUserGroup, faCalendar, faBookOpen, faList,
    faLayerGroup, faBoxArchive, faQuestion, faClock, faClipboardCheck);

const routes = [
  {path: '/divergen', component: AnalysisListingView},
  {path: '/divergen/analysis/create', component: AnalysisCreateView},
  {path: '/divergen/about', component: AboutView},
  {path: '/:pathMatch(.*)', component: NotFoundView},
  {path: '/analysis/:analysis_name', name: 'analysis', component: AnalysisView, props: true},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const app = createApp(App);

app.use(router);
app.component('font-awesome-icon', FontAwesomeIcon);
app.mount('#app');
