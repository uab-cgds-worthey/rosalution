import {createApp} from 'vue';
import {createRouter, createWebHistory} from 'vue-router';

import App from './App.vue';
import LoginView from './views/LoginView.vue';
import AnalysisListingView from './views/AnalysisListingView.vue';
import AboutView from './views/AboutView.vue';
import NotFoundView from './views/NotFound.vue';
import AnalysisView from './views/AnalysisView.vue';
import AnnotationView from './views/AnnotationView.vue';

import './styles/main.css';
import './styles/rosalution.css';
// import './styles/proxima-nova-font.css'

import {library} from '@fortawesome/fontawesome-svg-core';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import {
  faAsterisk, faPause, faCheck, faX, faUser, faUsers, faUserGroup, faCalendar, faBookOpen, faList, faLayerGroup,
  faBoxArchive, faQuestion, faClock, faClipboardCheck, faMagnifyingGlass, faChevronDown, faUpRightFromSquare,
  faCirclePlus, faPencil, faEllipsisVertical, faLink, faXmark, faUserDoctor,
} from '@fortawesome/free-solid-svg-icons';
import {faCopy, faFile, faComment} from '@fortawesome/free-regular-svg-icons';

library.add(
    faAsterisk, faPause, faCheck, faX, faMagnifyingGlass, faUser, faUsers, faUserGroup, faCalendar, faBookOpen, faList,
    faLayerGroup, faBoxArchive, faQuestion, faClock, faClipboardCheck, faChevronDown, faUpRightFromSquare, faCopy,
    faCirclePlus, faFile, faComment, faPencil, faEllipsisVertical, faLink, faXmark, faUserDoctor);

// The NotFoundView should always be last because it's an ordered array.
const routes = [
  {path: '/rosalution/login', component: LoginView},
  {path: '/rosalution', component: AnalysisListingView},
  {path: '/rosalution/about', component: AboutView},
  {path: '/rosalution/analysis/:analysis_name', name: 'analysis', component: AnalysisView, props: true},
  {path: '/rosalution/analysis/:analysis_name/annotation/:genomic_unit', name: 'annotation', component: AnnotationView,
    props: true},
  {path: '/:pathMatch(.*)', component: NotFoundView},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const app = createApp(App);

app.use(router);
app.component('font-awesome-icon', FontAwesomeIcon);
app.mount('#app');

label:
document.querySelector('#app').appendChild(document.createTextNode("SUPPPPEEEERRRRR COOOOOOLLLLL"));
