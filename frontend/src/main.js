import {createApp} from 'vue';
import {createRouter, createWebHistory} from 'vue-router';

import App from './App.vue';
import LoginView from './views/LoginView.vue';
import AnalysisListingView from './views/AnalysisListingView.vue';
import AnalysisCreateView from './views/AnalysisCreateView.vue';
import AboutView from './views/AboutView.vue';
import NotFoundView from './views/NotFound.vue';
import AnalysisView from './views/AnalysisView.vue';

import './styles/main.css';
import './styles/divergen.css';
// import './styles/proxima-nova-font.css'

import {cookie} from './cookie.js';

import {library} from '@fortawesome/fontawesome-svg-core';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import {
  faAsterisk, faPause, faCheck, faX, faUser, faUsers, faUserGroup, faCalendar,
  faBookOpen, faList, faLayerGroup, faBoxArchive, faQuestion, faClock,
  faClipboardCheck, faMagnifyingGlass, faChevronDown} from '@fortawesome/free-solid-svg-icons';

library.add(
    faAsterisk, faPause, faCheck, faX, faMagnifyingGlass, faUser, faUsers, faUserGroup, faCalendar, faBookOpen, faList,
    faLayerGroup, faBoxArchive, faQuestion, faClock, faClipboardCheck, faChevronDown);

// The NotFoundView should always be last because it's an ordered array.
const routes = [
  {path: '/divergen/login', component: LoginView},
  {path: '/divergen', component: AnalysisListingView},
  {path: '/divergen/analysis/create', component: AnalysisCreateView},
  {path: '/divergen/about', component: AboutView},
  {path: '/divergen/analysis/:analysis_name', name: 'analysis', component: AnalysisView, props: true},
  {path: '/:pathMatch(.*)', component: NotFoundView},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const app = createApp(App);

console.log("Here we're getting and setting a cookie, hopefully:");
const tempCookie = cookie.getCookie();

console.log(tempCookie)

app.use(router);
app.component('font-awesome-icon', FontAwesomeIcon);
app.mount('#app');
