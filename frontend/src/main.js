import {createApp} from 'vue';
import {createRouter, createWebHistory} from 'vue-router';

import App from './App.vue';
import LoginView from './views/LoginView.vue';
import LogoutView from './views/LogoutView.vue';
import AnalysisListingView from './views/AnalysisListingView.vue';
import FileView from './views/FileView.vue';
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
import {FontAwesomeIcon, FontAwesomeLayers} from '@fortawesome/vue-fontawesome';
import {
  faAsterisk, faPause, faCheck, faX, faUser, faUsers, faUserGroup, faCalendar, faBookOpen, faList, faLayerGroup,
  faBoxArchive, faQuestion, faClock, faClipboardCheck, faMagnifyingGlass, faChevronDown, faChevronRight,
  faUpRightFromSquare, faCirclePlus, faPencil, faEllipsisVertical, faLink, faXmark, faUserDoctor, faPaperclip, faPlus,
  faAnglesRight, faFileImage, faFileCirclePlus, faMountainSun, faArrowUp, faArrowDown, faCaretDown
} from '@fortawesome/free-solid-svg-icons';
import {
  faCopy, faFile, faComment, faCircleCheck, faCircleQuestion, faCircleXmark, faImages,
} from '@fortawesome/free-regular-svg-icons';

library.add(
    faAsterisk, faPause, faCheck, faX, faMagnifyingGlass, faUser, faUsers, faUserGroup, faCalendar, faBookOpen, faList,
    faLayerGroup, faBoxArchive, faQuestion, faClock, faClipboardCheck, faChevronDown, faChevronRight,
    faUpRightFromSquare, faCopy, faCirclePlus, faFile, faComment, faPencil, faEllipsisVertical, faLink, faXmark,
    faUserDoctor, faPaperclip, faPlus, faAnglesRight, faCircleCheck, faCircleQuestion, faCircleXmark, faImages,
    faFileImage, faFileCirclePlus, faMountainSun, faArrowUp, faArrowDown, faCaretDown
);

// The NotFoundView should always be last because it's an ordered array.
/* Placeholder route, name subject to change */
const routes = [
  {path: '/rosalution/login', name: 'login', component: LoginView},
  {path: '/rosalution', component: AnalysisListingView},
  {path: '/rosalution/account', name: 'account', component: AccountView},
  {path: '/rosalution/analysis/:analysis_name', name: 'analysis', component: AnalysisView, props: true},
  {path: '/rosalution/analysis/file/:file_id', name: 'file', component: FileView, props: true},
  {path: '/rosalution/analysis/:analysis_name/annotation/', name: 'annotation', component: AnnotationView, props: true},
  {path: '/rosalution/logout', name: 'logout', component: LogoutView},
  {path: '/:pathMatch(.*)', component: NotFoundView},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


/*
  This code is a placeholder for the user authorization. When the user navigates to their user info page, the
  router will use a new named route and fetch a special user object that contains their client_id and client_secret
  to display on the page. All of this is handled in stores/authStore.js
*/
router.beforeEach(async (to) => {
  const token = authStore.getToken();

  if (!token && to.name !== 'login') {
    return {name: 'login'};
  } else if (token && to.name == 'account') {
    const response = await authStore.getAPICredentials();

    if (response.error) {
      authStore.clearState();
      return {name: 'login'};
    }

    authStore.saveState(response);
  } else if (to.name == 'logout') {
    authStore.clearState();
  } else if (token) {
    const response = await authStore.verifyToken();

    if (response.error) {
      authStore.clearState();
      return {name: 'login'};
    }

    authStore.saveState(response);
  }
});

const app = createApp(App);

app.use(router);
app.component('font-awesome-icon', FontAwesomeIcon);
app.component('font-awesome-layers', FontAwesomeLayers);
app.component('AppFooter', footer);
app.mount('#app');
