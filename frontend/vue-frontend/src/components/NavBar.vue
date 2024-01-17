<template>
  <nav class="navbar navbar-expand-lg  navbar-dark bg-dark p-3">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand ">HOME</router-link>

      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
        aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link v-if="isAuthenticated" to="/appointments/view" class="nav-link">My Appointments</router-link>
          </li>
        </ul>

        <form class="d-flex">
          <button v-if="isAuthenticated" class="btn btn-danger" @click="logOut">Logout</button>
        </form>
      </div>
    </div>
  </nav>
</template>

<script>
import authService from '@/services/AuthService';

export default {
  name: 'NavBar',
  components: {
  },
  data() {
    return {
      isAuthenticatedData: false,
    }
  },
  created() {
    this.isAuthenticatedData = authService.isAuthenticated();
  },
  computed: {
    isAuthenticated() {
      return this.isAuthenticatedData;
    }
  },
  methods: {
    logOut() {
      console.log('i am logging out');
      authService.logout();
      this.isAuthenticatedData = authService.isAuthenticated();
      if (this.$route.path != "/") {
        this.$router.push("/");
      }

      // Clear all items in localStorage
      localStorage.clear();
      console.log("Local storage cleared!");
    },
    clearLocalStorage() {
      // Clear all items in localStorage
      localStorage.clear();
      console.log("Local storage cleared!");
    }
  }
}
</script>