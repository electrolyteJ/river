import { WelcomePage, VideoPage } from './';

export default {
  path: '',
  childRoutes: [
    { path: 'video-page', component: VideoPage, isIndex: true },
    { path: 'welcome-page', component: WelcomePage, isIndex: false }
  ],
};
