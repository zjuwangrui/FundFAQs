import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      // Must come before /:id to avoid "new" matching the int param
      path: '/article/new',
      name: 'new-article',
      component: () => import('../views/EditArticleView.vue'),
    },
    {
      path: '/article/:id/edit',
      name: 'edit-article',
      component: () => import('../views/EditArticleView.vue'),
    },
    {
      path: '/article/:id',
      name: 'article-detail',
      component: () => import('../views/ArticleDetailView.vue'),
    },
  ],
})

export default router
