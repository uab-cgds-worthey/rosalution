import {createApp} from 'vue';
import {createRouter, createWebHistory} from 'vue-router';

import App from './App.vue';
import LoginView from './views/LoginView.vue';
import LogoutView from './views/LogoutView.vue';
import AnalysisListingView from './views/AnalysisListingView.vue';
import NotFoundView from './views/NotFound.vue';
import AccountView from './views/AccountView.vue';
import AnalysisView from './views/AnalysisView.vue';
import AnnotationView from './views/AnnotationView.vue';

import footer from './components/AppFooter.vue';

import './styles/main.css';
import './styles/rosalution.css';
// import './styles/proxima-nova-font.css'

import {authStore} from '@/stores/authStore.js';
import {library} from '@fortawesome/fontawesome-svg-core';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import {
  faAsterisk, faPause, faCheck, faX, faUser, faUsers, faUserGroup, faCalendar, faBookOpen, faList, faLayerGroup,
  faBoxArchive, faQuestion, faClock, faClipboardCheck, faMagnifyingGlass, faChevronDown, faChevronRight,
  faUpRightFromSquare, faCirclePlus, faPencil, faEllipsisVertical, faLink, faXmark, faUserDoctor, faPaperclip, faPlus,
  faAnglesRight,
} from '@fortawesome/free-solid-svg-icons';
import {faCopy, faFile, faComment} from '@fortawesome/free-regular-svg-icons';

library.add(
    faAsterisk, faPause, faCheck, faX, faMagnifyingGlass, faUser, faUsers, faUserGroup, faCalendar, faBookOpen, faList,
    faLayerGroup, faBoxArchive, faQuestion, faClock, faClipboardCheck, faChevronDown, faChevronRight,
    faUpRightFromSquare, faCopy, faCirclePlus, faFile, faComment, faPencil, faEllipsisVertical, faLink, faXmark,
    faUserDoctor, faPaperclip, faPlus, faAnglesRight);

// The NotFoundView should always be last because it's an ordered array.
const routes = [
  {path: '/rosalution/login', name: 'login', component: LoginView},
  {path: '/rosalution', component: AnalysisListingView},
  {path: '/rosalution/account', name: 'account ', component: AccountView},
  {path: '/rosalution/analysis/:analysis_name', name: 'analysis', component: AnalysisView, props: true},
  {path: '/rosalution/analysis/:analysis_name/annotation/', name: 'annotation', component: AnnotationView, props: true},
  {path: '/rosalution/logout', name: 'logout', component: LogoutView},
  {path: '/:pathMatch(.*)', component: NotFoundView},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to) => {
  const token = authStore.getToken();

  if (!token && to.name !== 'login') {
    return {name: 'login'};
  } else if (token) {
    const response = await authStore.verifyToken();
    authStore.saveState(response);
  }
});

const app = createApp(App);

app.use(router);
app.component('font-awesome-icon', FontAwesomeIcon);
app.component('AppFooter', footer);
app.mount('#app');
