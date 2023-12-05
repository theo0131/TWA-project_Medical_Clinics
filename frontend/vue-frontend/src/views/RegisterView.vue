<template>
    <div id="app">
        <div class="register-container">
        <h2>Register</h2>
        <div class="form-group">
            <label for="username">Username:</label>
            <input type="text" id="username" v-model="username" class="input-field">
        </div>
        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" v-model="email" class="input-field">
        </div>
        <div class="form-group">
            <label for="role">Role:</label>
            <select id="role" v-model="role" class="input-field">
            <option value="patient">Patient</option>
            <option value="doctor">Doctor</option>
            </select>
        </div>
        <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" id="password" v-model="password" class="input-field">
        </div>
        <div class="form-group">
            <label for="confirmPassword">Confirm Password:</label>
            <input type="password" id="confirmPassword" v-model="confirmPassword" class="input-field">
        </div>
        <div class="form-group">
            <button @click="register" class="btn">Register</button>
        </div>
        <p v-if="error" class="error-msg">{{ error }}</p>
        <p v-if="success" class="success-msg">{{ success }}</p>
        </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';

  export default {
    name: 'RegisterView',
    data() {
      return {
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        role: '',
        error: '',
        success: ''
      };
    },
    mounted() {
    },
    methods: {
      async register() {
        // Simulating registration functionality (replace this with actual validation and backend logic)
        if (
          this.username !== '' &&
          this.email !== '' &&
          this.password !== '' &&
          this.password === this.confirmPassword
        ) {
          console.log(this.username, this.password)
          await axios.post('http://127.0.0.1:5000/register', {
            username: this.username,
            password: this.password,
            email: this.email,
            role: this.role
          });
          // Registration successful
          this.success = 'Registration successful';
          // You can redirect to another page or perform other actions after successful registration
        } else {
          // Registration failed
          this.error = 'Please fill in all fields correctly';
          console.log(this.error)
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
    .register-container {
      background-color: white;
      padding: 20px;
      border-radius: 5px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      max-width: 200px;
    }
    .form-group {
      margin-bottom: 15px;
    }
    .form-group label {
      display: block;
      font-weight: bold;
      margin-bottom: 5px;
    }
    .form-group input,
    .form-group select {
      width: calc(100% - 16px); /* Adjust width for border and padding */
      padding: 8px;
      border: 1px solid #ccc;
      border-radius: 4px;
      box-sizing: border-box; /* Ensure padding is included in the width */
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