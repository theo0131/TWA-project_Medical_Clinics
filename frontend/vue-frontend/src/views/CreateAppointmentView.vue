<template>
    <div id="app">
      <h1>Welcome to the Medical Appointment System</h1>
      <div>
        <h2>Make an Appointment</h2>
        <form @submit.prevent="scheduleAppointment">
          <div class="form-group">
              <label for="patientName" class="form-group">Patient Name:</label>
              <input type="text" v-model="appointment.patientName" class="form-group">
          </div>
          <div class="form-group">
              <label for="doctor" class="form-group">Doctor:</label>
              <select v-model="selectedUserIndex" id="userSelect">
                <option v-for="(doctor, index) in doctors" :key="index">
                  {{ doctor.name }}
                </option>
              </select>
              <p>Selected User Index: {{ selectedUserIndex }}</p>
              <p>Selected User: {{ doctors[selectedUserIndex]?.name }}</p>
          </div>
          <div class="form-group">
              <label for="appointmentDate" class="form-group">Appointment Date:</label>
              <input type="datetime-local" v-model="appointment.appointmentDate" class="form-group">
          </div>
          <div class="form-group">
              <button type="submit" class="form-group">Schedule Appointment</button>
          </div>
        </form>
        <p v-if="successMessage" style="color: green;">{{ successMessage }}</p>
        <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
      </div>
    </div>
  </template>
  
<script>
import axios from 'axios';

export default {
  name: 'CreateAppointment',
  data() {
    return {
      appointment: {
        patientName: '',
        appointmentDate: ''
      },
      doctors: [],
      successMessage: '',
      errorMessage: '',
      selectedUserIndex: null,
    };
  },
  mounted() {
        // Retrieve JWT token from localStorage
        const token = localStorage.getItem('token');

        if (token) {
          // If token exists, make an authenticated request to get doctors
          axios.get('http://127.0.0.1:5000/doctors', {
            headers: {
              Authorization: `Bearer ${token}`
            }
          })
          .then(response => {
            // Handle successful response and populate doctors data
            this.doctors = response.data;
          })
          .catch(error => {
            // Handle error (e.g., authentication failure or unauthorized access)
            console.error('Error fetching doctors:', error);
          });
        } else {
          // Token doesn't exist in localStorage, handle accordingly
          console.log('No token found in localStorage');
          // For example, redirect to login page
          // window.location.href = '/login';
        }
  },
  methods: {
    scheduleAppointment() {
      // Logic to schedule appointment
      // Include the token in the request headers for authentication
      const token = localStorage.getItem('token');
      if (token) {
        axios.post('http://127.0.0.1:5000/appointments/create', this.appointment, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        .then(response => {
          // Handle successful appointment scheduling
          this.successMessage = 'Appointment scheduled successfully!';
          console.log(response.data);
          this.clearForm();
        })
        .catch(error => {
          // Handle error (e.g., authentication failure or unauthorized access)
          console.error('Error scheduling appointment:', error);
          this.errorMessage = 'Failed to schedule appointment. Please try again.';
        });
      } else {
        console.log('No token found in localStorage');
        // Handle case where token is missing (redirect to login, show error message, etc.)
      }
    },
    clearForm() {
      // Function to clear the form after successful submission
      this.appointment.patientName = '';
      this.appointment.doctor = '';
      this.appointment.appointmentDate = '';
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
  