<template>
    <div>
        <NavBar></NavBar>
        
        <div class="container mt-5">
            <div class="container">
                <div class="row">
                    <div class="col">
                        <h2>Your Appointments</h2>
                    </div>
                    <div class="col-auto p-0 d-flex align-items-center" v-if="userType === 'pacient'">
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
                            <h5 class="card-title" v-if="userType === 'doctor'">
                                Appointment with pacient {{ appointment.pacient }}
                            </h5>
                            <h5 class="card-title" v-else>
                                Appointment with doctor {{ appointment.doctor }}
                            </h5>  
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
        userType: "",
        clientAppointments: [],
        };
    },
    mounted() {
        // Retrieve JWT token from localStorage
        console.log(localStorage)
        console.log(localStorage.getItem('token'))
        const token = localStorage.getItem('token');

        if (token) {
            // If token exists, make an authenticated request to get doctors

                axios.get('http://127.0.0.1:5000/appointments', {
                    headers: {
                        Authorization: `${token}`
                    }
                })
                .then(response => {
                    // Handle successful response and populate doctors data
                    this.clientAppointments = response.data.appointments;
                    this.userType = response.data.userType;
                })
                .catch(error => {
                    // Handle error (e.g., authentication failure or unauthorized access)
                    console.error('Error fetching doctors:', error);
                });
            // TODO: ia din database appointmenturile
        } else {
            // Token doesn't exist in localStorage, handle accordingly
            console.log('No token found in localStorage for AppointmentsView');
            // Handle case where token is missing (redirect to login, show error message, etc.)
            this.$router.push("/");
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
    