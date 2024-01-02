<template>
    <div>
      <NavBar></NavBar>
      <div class="register-container form mx-auto mt-4 p-5">
        <h2>Register</h2>
        <br>
        <div class="form-group-1">
            <label for="username">First Name:</label>
            <input type="text" id="username" v-model="firstName" class="input-field">
        </div>
        <div class="form-group-1">
            <label for="username">Last Name:</label>
            <input type="text" id="username" v-model="lastName" class="input-field">
        </div>
        <div class="form-group-1">
            <label for="email">Email:</label>
            <input type="email" id="email" v-model="email" class="input-field">
        </div>

        <div class="form-group-1">
            <label for="role">Role:</label>
            <select id="role" v-model="selectedRole" class="input-field">
            <option value="pacient">Pacient</option>
            <option value="doctor">Doctor</option>
            </select>
        </div>

        <div v-if="selectedRole == 'pacient'" class="form-group-1">
              <label for="appointmentDate" >Age:</label>
              <input type="number" v-model="age">
        </div>

        <div class="form-group" v-if="selectedRole == 'pacient'">
            <label class="gender-label" for="gender">Gender:</label>
            <div class="form-check form-check-inline">
              <input v-model="gender" class="form-check-input" type="radio" name="gender" id="male" value="M">
              <label class="form-check-label" for="male">Male</label>
            </div>
            <div class="form-check form-check-inline">
              <input v-model="gender" class="form-check-input" type="radio" name="gender" id="female" value="F">
              <label class="form-check-label" for="female">Female</label>
            </div>
        </div>

        <div v-if="selectedRole == 'doctor'" class="form-group-1">
            <label for="role">Specialty:</label>
            <select id="role" v-model="selectedSpecialty" class="input-field">
              <option v-for="specialty in specialties" :key="specialty.id">
                  {{ specialty.name }}
                </option>
            </select>
        </div>

        <div class="form-group-1">
            <label for="password">Password:</label>
            <input type="password" id="password" v-model="password" class="input-field">
        </div>
        <div class="form-group-1">
            <label for="confirmPassword">Confirm Password:</label>
            <input type="password" id="confirmPassword" v-model="confirmPassword" class="input-field">
        </div>
        <div class="form-group-1">
            <button @click="register" class="btn">Register</button>
        </div>
        <p v-if="error" class="error-msg">{{ error }}</p>
        <p v-if="success" class="success-msg">{{ success }}</p>
      </div>
    </div>
</template>
  
<script>
import axios from 'axios';

import NavBar from '@/components/NavBar.vue'

  export default {
    name: 'RegisterView',
    components:{
      NavBar
    },
    data() {
      return {
        firstName: '',
        lastName: '',
        gender: '',
        email: '',
        password: '',
        confirmPassword: '',
        selectedRole: '',
        selectedSpecialty: '',
        error: '',
        success: '',
        age: '',
        specialties: []
      };
    },
    mounted() {
      axios.get('http://127.0.0.1:5000/specialties')
          .then(response => {
            // Handle successful response and populate doctors data
            this.specialties = response.data;
          })
          .catch(error => {
            // Handle error (e.g., authentication failure or unauthorized access)
            console.error('Error fetching doctors:', error);
          });
    },
    methods: {
      async register() {
        var response = null;
        console.log(this.selectedSpecialty);
        // Simulating registration functionality (replace this with actual validation and backend logic)
        if (
          this.firstName !== '' &&
          this.lastName !== '' &&
          this.email !== '' &&
          this.password !== '' &&
          this.password === this.confirmPassword &&
          !(this.selectedRole == "doctor" && this.selectedSpecialty == '')
        ) {
          // Registration successful

          console.log(this.DOB);
          response = await axios.post('http://127.0.0.1:5000/register', {
            firstName: this.firstName,
            lastName: this.lastName,
            gender: this.gender,
            email: this.email,
            password: this.password,
            role: this.selectedRole,
            specialty: this.selectedSpecialty,
            age: this.age,
          });
        }

        if (response) {
          this.success = 'Registration successful';
          // You can redirect to another page or perform other actions after successful registration
        } else {
          // Registration failed
          this.error = 'Please fill in all fields correctly';
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
      max-width: 500px;
    }
    .form-group-1 {
      margin-bottom: 15px;
    }
    
    .form-group {
      margin-bottom: 15px;
    }

    .form-group-1 label {
      display: block;
      font-weight: bold;
      margin-bottom: 5px;
    }

    .gender-label {
      display: block;
      font-weight: bold;
      margin-bottom: 5px;
    }
    .form-group-1 input,
    .form-group-1 select {
      width: calc(100% - 16px); /* Adjust width for border and padding */
      padding: 8px;
      border: 1px solid #ccc;
      border-radius: 4px;
      box-sizing: border-box; /* Ensure padding is included in the width */
    }
    .form-group-1 button {
      padding: 8px 12px;
      background-color: #007bff;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
    .form-group-1 button:hover {
      background-color: #0056b3;
    }
</style>
  