import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SearchView from '../views/SearchView.vue'
import SearchResultsView from '../views/SearchResultsView.vue'
import BrowseView from '../views/BrowseView.vue'
import CompoundDetailView from '../views/CompoundDetailView.vue'
import SubmitView from '../views/SubmitView.vue'
import HelpView from '../views/HelpView.vue'
import StatisticsView from '../views/StatisticsView.vue'
import DownloadView from '../views/DownloadView.vue'
import FungusDetailView from '../views/FungusDetailView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/search',
    name: 'search',
    component: SearchView
  },
  {
    path: '/results',
    name: 'results',
    component: SearchResultsView
  },
  {
    path: '/browse',
    name: 'browse',
    component: BrowseView
  },
  {
    path: '/compound/:id',
    name: 'compound-detail',
    component: CompoundDetailView,
    props: true
  },
  {
    path: '/fungus/:id',
    name: 'fungus-detail',
    component: FungusDetailView,
    props: true
  },
  {
    path: '/submit',
    name: 'submit',
    component: SubmitView
  },
  {
    path: '/help',
    name: 'help',
    component: HelpView
  },
  {
    path: '/statistics',
    name: 'statistics',
    component: StatisticsView
  },
  {
    path: '/download',
    name: 'download',
    component: DownloadView
  }
]

const router = createRouter({
  history: createWebHistory('/pmmdb/'),
  routes
})

export default router