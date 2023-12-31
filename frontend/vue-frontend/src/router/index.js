import Vue from 'vue';
import VueRouter from 'vue-router';
import HomeView from '../views/HomeView.vue';
import AboutView from '../views/AboutView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import CreateAppointmentView from '../views/CreateAppointmentView.vue';
import AppointmentsView from '../views/AppointmentsView.vue'

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'HomeView',
    component: HomeView,
  },
  {
    path: '/about',
    name: 'AboutView',
    component: AboutView,
  },
  {
    path: '/login',
    name: 'LoginView',
    component: LoginView,
  },
  {
    path: '/register',
    name: 'RegisterView',
    component: RegisterView,
  },
  {
    path: '/appointments',
    name: 'AppointmentsView',
    component: AppointmentsView,
    children: [
      {
        path: 'create',
        name: 'CreateAppointments',
        component: CreateAppointmentView,
      },
    ]
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;