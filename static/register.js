new Vue({
    el: '#app',
    data: {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      selectedRole: '',
      error: '',
      success: ''
    },
    methods: {
      register() {
        // Simulating registration functionality (replace this with actual validation and backend logic)
        if (
          this.username !== '' &&
          this.email !== '' &&
          this.password !== '' &&
          this.password === this.confirmPassword
        ) {
          // Registration successful
          this.success = 'Registration successful';
          // You can redirect to another page or perform other actions after successful registration
        } else {
          // Registration failed
          this.error = 'Please fill in all fields correctly';
        }
      }
    }
  });