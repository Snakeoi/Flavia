import { createRouter, createWebHistory } from 'vue-router'
import HomeView from "@/views/HomeView.vue";
import NotFound from "@/views/NotFound.vue";
import AdminView from "@/views/admin/AdminView.vue";
import UsersView from "@/views/admin/Users/UsersView.vue";
import UserViewCreate from "@/views/admin/Users/UserViewCreate.vue";
import UserView from "@/views/admin/Users/UserView.vue";


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/:catchAll(.*)',
      component: NotFound
    },
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/admin',
      name: 'admin-dashboard',
      component: AdminView,
      children: [
        {
          path: 'users',
          name: 'admin-users',
          component: UsersView,
        },
        {
          path: 'user/:id(\\d+)',
          name: 'admin-user',
          component: UserView,
        },
        {
          path: 'user/',
          name: 'admin-user-add',
          component: UserViewCreate,
        }
      ]
    }
  ]
})

export default router
