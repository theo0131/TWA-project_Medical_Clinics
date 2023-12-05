<template>
    <body>
        <div id="app">
            <div class="login-container">
                <h2>Login</h2>
                <div class="form-group">
                    <label for="username">Username:</label>
                    <input type="text" id="username" v-model="username">
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" v-model="password">
                </div>
                <div class="form-group">
                    <button @click="login">Login</button>
                </div>
                <p v-if="error" style="color: red;">{{ error }}</p>
            </div>
        </div>
    </body>
</template>

<script>
import axios from 'axios';

export default {
    name: 'LoginView',
    data() {
        return {
            username: '',
            password: '',
            error: ''
        };
    },
    mounted() {
    },
    methods: {
      async login() {
        try{
          const response = await axios.post('http://127.0.0.1:5000/login', {
            username: this.username,
            password: this.password
          });

          // Assuming your backend responds with a JWT token
          const token = response.data.token;

          // Store the token securely (local storage, Vuex, etc.)
          localStorage.setItem('token', token);
        } catch (error) {
          this.error = 'Invalid credentials. Please try again.';
          console.log(error)
        }
      }
    }
};
</script>

<style scoped>
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
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
  