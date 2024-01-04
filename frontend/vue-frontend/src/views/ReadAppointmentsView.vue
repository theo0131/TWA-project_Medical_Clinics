<template>
    <div>
        <NavBar></NavBar>
        
        <div class="container mt-5">
            <div class="container">
                <div class="row">
                    <div class="col">
                        <h2>Your Appointments</h2>
                    </div>
                    <div class="col-auto p-0 d-flex align-items-center">
                        <button  class="btn btn-success " @click="createAppointmentButtonHandle">+ Add Appointment</button>
                    </div>
                </div>
            </div>

            <hr>
            <br>
            <div class="row">
                <div v-for="appointment in clientAppointments" :key="appointment.id" class="col-md-4 mb-4">
                    <div class="card" @click="viewAppointment(appointment)">
                        <div class="card-body">
                            <!-- Display appointment details here -->
                            <h5 class="card-title">{{ appointment.title }}</h5>
                            <p class="card-text">{{ appointment.date }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script>
import axios from 'axios';
import NavBar from '@/components/NavBar.vue';

export default {
    name: 'ReadAppointments',
    components: {
        NavBar
    },
    data() {
        return {
        clientAppointments: [
            { id: 1, title: 'Appointment 1', date: '2023-01-01' },
            { id: 2, title: 'Appointment 2', date: '2023-02-01' },
            { id: 3, title: 'Appointment 3', date: '2023-02-01' },
            { id: 4, title: 'Appointment 4', date: '2023-02-01' },
            { id: 5, title: 'Appointment 5', date: '2023-02-01' },
            // Add more appointments as needed
        ],
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
        createAppointmentButtonHandle() {
            this.$router.push("/appointments/create");
        }
        ,
        clearForm() {
            // Function to clear the form after successful submission
            this.appointment.patientName = '';
            this.appointment.doctor = '';
            this.appointment.appointmentDate = '';
        },
        viewAppointment(appointment) {
            this.$router.push(`/appointment/${appointment.id}`);
            // Perform actions when the card is clicked
            console.log("Clicked card:", appointment);
            // You can add your custom logic here based on the clicked appointment
        }
    }
};
</script>
  
<style scoped></style>
    