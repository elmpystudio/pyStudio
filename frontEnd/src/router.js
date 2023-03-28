import Vue from 'vue';
import Router from 'vue-router';
import Landing from '@/views/Landing';
import DashboardView from '@/views/DashboardView';
import VisualAnalyticsView from '@/views/VisualAnalyticsView';
import EditAnalytics from '@/views/EditAnalytics';
import ViewAnalytics from '@/views/ViewAnalytics';
import CreateAnalyticsView from '@/views/CreateAnalyticsView';
import MarketplaceView from '@/views/MarketplaceView';
import MarketplaceItem from '@/views/MarketplaceItem';
import VAOffering from '@/views/Marketplace/VAOffering';
import DatasetView from '@/views/DatasetView';
import PublishOffering from '@/views/PublishOffering';
import EditDataset from '@/views/EditDataset';
import PublishVA from '@/views/PublishVA';
import Notifications from '@/views/NotificationsView';
import Profile from '@/views/Profile';
import MachineLearningView from '@/views/MachineLearningView';
import Notebook from '@/views/NotebookView';
import Administration from '@/views/AdministrationView';

Vue.use(Router);

const router = new Router({
    mode: 'history',
    routes: [
        { path: '/', name: 'dashboard', component: DashboardView },
        { path: '/landing', name: 'landing', component: Landing },
        { path: '/visual-analytics', name: 'analytics', component: VisualAnalyticsView },
        { path: '/visual-analytics/:name/view', name: 'analytics-view', component: ViewAnalytics },
        { path: '/visual-analytics/:name/edit', name: 'analytics-edit', component: EditAnalytics },
        { path: '/visual-analytics/create/:projectId', name: 'analytics-create', component: CreateAnalyticsView },
        { path: '/marketplace', name: 'marketplace', component: MarketplaceView },
        { path: '/marketplace/dataset/:id', name: 'dataset-offering', component: MarketplaceItem },
        { path: '/marketplace/va/:id', name: 'va-offering', component: VAOffering },
        { path: '/dataset/:id', name: 'dataset', component: DatasetView },
        { path: '/dataset/:id/publish', name: 'dataset-publish', component: PublishOffering },
        { path: '/dataset/:id/edit', name: 'dataset-edit', component: EditDataset },
        { path: '/visual-analytics/:id/publish', name: 'analytics-publish', component: PublishVA },
        { path: '/notifications', name: 'notifications', component: Notifications },
        { path: '/profile', name: 'profile', component: Profile },
        { path: '/ml', name: 'machine-learning', component: MachineLearningView },
        { path: '/notebook', name: 'notebook', component: Notebook },
        { path: '/administration', name: 'administration', component: Administration },
    ],
});

router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem('token');
    if (to.name !== 'landing' && !isAuthenticated) {
        next({ name: 'landing' })
    } else {
        next();
    }
});

export default router;
