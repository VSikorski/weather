import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RetrieveView from '../views/RetrieveView.vue'
import DeleteView from '@/views/DeleteView.vue'
import InsertView from '@/views/InsertView.vue'
import UpdateView from '@/views/UpdateView.vue'
import MonthlyView from '@/views/MonthlyView.vue'
import UploadFile from '@/components/UploadFile.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/apiR',
      name: 'Retrieve',
      component: RetrieveView,
    },
    {
      path: '/apiD',
      name: 'Delete',
      component: DeleteView,
    },
    {
      path: '/apiI',
      name: 'Insert',
      component: InsertView,
    },
    {
      path: '/apiU',
      name: 'Update',
      component: UpdateView,
    },
    {
      path: '/monthly',
      name: 'Monthly',
      component: MonthlyView,
    },
    {
      path: '/upload',
      name: 'Upload',
      component: UploadFile,
    }
  ],
})

export default router
