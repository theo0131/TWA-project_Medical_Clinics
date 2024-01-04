<template>
  <div>
    <NavBar></NavBar>

    <div class="container mt-4">
      <h1>Welcome to the Medical Appointment System</h1><br>
      <div 
        style="max-width: 800px;"
        class="border p-4 mx-auto">
        <h2>You are viewing an Appointment</h2>
        <br>
        <form class="form">
          <div class="form-group">
              <label for="appointmentDate" >Appointment Id: </label>
              <input v-model="appointment.id" readonly>
          </div>
        </form>
      </div>
    </div>
  </div>
  </template>
  
  <script>

import axios from 'axios';
import NavBar from '@/components/NavBar.vue';

  export default {
    name: 'AppointmentView',
    components: {
        NavBar
    },
    data() {
      return {
        appointment: {
          id: 0
        }
      };
    },
    mounted() {
        console.log(localStorage)
        console.log(localStorage.getItem('token'))
        const token = localStorage.getItem('token');      if (token) {
        axios.get(`http://127.0.0.1:5000/api/appointments/${this.$route.params.id}`, {
            headers: {
              Authorization: `${token}`
            }
          })
        .then(response => {
          console.log(response.data);
          this.appointment.id = response.data.id;
        })
        .catch(error => {
          // Handle error (e.g., authentication failure or unauthorized access)
            console.error('Error fetching appointment:', error);
        });

      } else {
        console.log('No token found in localStorage');
        // Handle case where token is missing (redirect to login, show error message, etc.)
      }

    },
    methods: {
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
  .form-group button:hover {
    background-color: #0056b3;
  }
</style>
  