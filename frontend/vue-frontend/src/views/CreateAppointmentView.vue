<template>
  <div>
    <NavBar></NavBar>
    <div class="container mt-4">
      <h1>Welcome to the Medical Appointment System</h1><br>
      <div 
        style="max-width: 800px;"
        class="border p-4 mx-auto">
        <h2>Make an Appointment</h2>
        <br>
        <form
          class="form"
          @submit.prevent="scheduleAppointment">
          <div class="form-group">
              <label for="doctor">Doctor:</label>
              <select  id="userSelect" @change="handleChange">
                <option v-for="doctor in doctors" :key="doctor.medic_id" :value="doctor.medic_id">
                  {{ doctor.name }}
                </option>
              </select>
          </div>
          <div class="form-group">
              <label for="appointmentDate" >Appointment Date:</label>
              <input type="datetime-local" v-model="appointment.appointmentDate">
          </div>
          <div class="form-group">
              <label for="reason" >Reason:</label>
              <input v-model="appointment.reason">
          </div>
          <br>
          <div >
              <button type="submit" class="btn btn-primary">Schedule Appointment</button>
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
  name: 'CreateAppointment',
  components:{
    NavBar
  },
  data() {
    return {
      appointment: {
        doctor_id: 1,
        appointmentDate: '',
        reason: ''
      },
      doctors: [],
      successMessage: '',
      errorMessage: '',
    };
  },
  mounted() {
        // Retrieve JWT token from localStorage
        console.log(localStorage)
        console.log(localStorage.getItem('token'))
        const token = localStorage.getItem('token');

        if (token) {
          // If token exists, make an authenticated request to get doctors
          axios.get('http://127.0.0.1:5000/doctors', {
            headers: {
              Authorization: `${token}`
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
          this.$router.push("/");
          // For example, redirect to login page
          // window.location.href = '/login';
        }
  },
  methods: {
    handleChange(e) {
        if(e.target.options.selectedIndex > -1) {
            this.appointment.doctor_id = this.doctors[e.target.options.selectedIndex].doctor_id
        }
    },
    scheduleAppointment() {
      // Logic to schedule appointment
      // Include the token in the request headers for authentication
      const token = localStorage.getItem('token');
      console.log(this.appointment.doctor_id);
      if (token) {
        axios.post('http://127.0.0.1:5000/appointments/create', this.appointment, {
          headers: {
            Authorization: `${token}`
          }
        })
        .then(response => {
          // Handle successful appointment scheduling
          this.successMessage = 'Appointment scheduled successfully!';
          console.log("De aici")
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
      this.appointment.doctor_id = '';
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
  .form-group button:hover {
    background-color: #0056b3;
  }
</style>
  