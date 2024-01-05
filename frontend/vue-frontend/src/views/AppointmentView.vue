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
        <form class="form" @submit.prevent="saveChanges">
          <div class="form-group">
              <label for="id" >Appointment Id: </label>
              <input v-model="appointment.id" readonly>
          </div>
          <div class="form-group">
              <label for="medic" >Medic: </label>
              <input v-model="appointment.medic" readonly>
          </div>
          <div class="form-group">
              <label for="pacient" >Pacient: </label>
              <input v-model="appointment.pacient" readonly>
          </div>
          <div class="form-group">
              <label for="time" >Time: </label>
              <input v-model="appointment.time" readonly>
          </div>
          <div class="form-group">
              <label for="reason" >Reason: </label>
              <input v-model="appointment.reason" readonly>
          </div>
          <div class="form-group">
              <label for="diagnostic" >Diagnostic: </label>
              <input v-model="appointment.diagnostic" :readonly="isDiagnosticReadOnly">
          </div>
          <br>
          <div v-if="appointment.userType === 'doctor'">
              <button class="btn btn-primary">Save Changes</button>
          </div>
        </form>
        <p v-if="successMessage" style="color: green;">{{ successMessage }}</p>
        <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
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
          id: 0,
          medic: "",
          pacient: "",
          time: "",
          reason: "",
          diagnostic: "",
          userType: ""
        },
        successMessage: '',
        errorMessage: '',
      };
    },
    mounted() {
        this.successMessage = "";
        this.errorMessage = "";
        console.log(localStorage)
        console.log(localStorage.getItem('token'))
        const token = localStorage.getItem('token');
        if (token) {
        axios.get(`http://127.0.0.1:5000/api/appointments/${this.$route.params.id}`, {
            headers: {
              Authorization: `${token}`
            }
          })
        .then(response => {
          console.log(response.data);
          this.appointment.id = response.data.id;
          this.appointment.medic = response.data.medic;
          this.appointment.pacient = response.data.pacient;
          this.appointment.time = response.data.time;
          this.appointment.reason = response.data.reason;
          this.appointment.diagnostic = response.data.diagnostic;
          this.appointment.userType = response.data.userType;
        })
        .catch(error => {
          // Handle error (e.g., authentication failure or unauthorized access)
            console.error('Error fetching appointment:', error);
        });

      } else {
        console.log('No token found in localStorage');
        // Handle case where token is missing (redirect to login, show error message, etc.)
        this.$router.push("/");
      }

    },
    methods: {
      saveChanges() {
      this.successMessage = "";
      this.errorMessage = "";
      // Logic to schedule appointment
      // Include the token in the request headers for authentication
      const token = localStorage.getItem('token');
      console.log("Update info");
      console.log(token);
      if (token) {
        axios.post('http://127.0.0.1:5000/appointments/update', this.appointment, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        .then(response => {
          // Handle successful appointment scheduling
          this.successMessage = 'Appointment updated successfully!';
          console.log("De aici")
          console.log(response.data);
        })
        .catch(error => {
          // Handle error (e.g., authentication failure or unauthorized access)
          console.error('Error scheduling appointment:', error);
          this.errorMessage = 'Failed to update the appointment. Please try again.';
        });
      } else {
        console.log('No token found in localStorage for AppointmentView');
        // Handle case where token is missing (redirect to login, show error message, etc.)
        this.$router.push("/login");
      }
    }
    },
    computed: {
      isDiagnosticReadOnly() {
        return this.appointment.userType !== "doctor";
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
  .form-group button:hover {
    background-color: #0056b3;
  }
</style>
  