<template>
  <div class="welcome-container">
    <div class="form-group">
      <h2>Welcome</h2>
      <div>
        <button @click="goTo('/login')">Login</button>
      </div>
      <div>
        <button @click="goTo('/register')">Register</button>
      </div>
    </div>
    <p v-if="error" style="color: red;">{{ error }}</p>
  </div>
</template>

<script>
export default {
  name: 'WelcomePage',
  data() {
    return {
      error: null
    };
  },
  mounted() {
    this.clearLocalStorage(); // Call your method here
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

<style>
/* Your CSS styles here */
.welcome-container {
  font-family: Arial, sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f4f4f4;
}

.login-container {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.form-group button {
  padding: 8px 12px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.form-group button:hover {
  background-color: #0056b3;
}
</style>