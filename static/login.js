new Vue({
    el: '#app',
    data: {
      username: '',
      password: '',
      error: ''
    },
    methods: {
      login() {
        // Simulating login functionality (replace this with actual authentication logic)
        if (this.username === 'user' && this.password === 'password') {
          // Login successful
          alert('Login successful');
          // You can redirect to another page or perform other actions after successful login
        } else {
          // Login failed
          this.error = 'Invalid username or password';
        }
      }
    }
  });