<template>
  <div>
    <NavBar></NavBar>
    <div class="container mt-4">
      <div 
        class="border p-4 text-center mx-auto"
        style="max-width: 600px;">
        <h2>Welcome</h2>
        <div
          class="container">
          <div>
            <button
              type="button"
              class="btn btn-primary m-2"
              @click="goTo('/login')">Login</button>
          </div>
          <div>
            <button 
              type="button"
              class="btn btn-success m-2"
              @click="goTo('/register')">Register</button>
          </div>
        </div>
      </div>
      <p v-if="error" style="color: red;">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';

export default {
  name: 'WelcomePage',
  components: {
    NavBar
  },
  data() {
    return {
      error: null
    };
  },
  mounted() {
    // this.clearLocalStorage(); // Call your method here
  },
  methods: {
    goTo(path) {
      this.$router.push(path);
    },
    clearLocalStorage() {
      // Clear all items in localStorage
      localStorage.clear();
    }
  }
};
</script>