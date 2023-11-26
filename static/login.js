new Vue({
    el: '#app',
    data: {
      username: '',
      password: '',
      error: ''
    },
    methods: {
      async login() {
        try{

          console.log("nu am trimis")

          const response = await axios.post('/login', {
            username: this.username,
            password: this.password
          });

          console.log("am trimis")
          // Assuming your backend responds with a JWT token
          const token = response.data.token;

          // Store the token securely (local storage, Vuex, etc.)
          localStorage.setItem('token', token);

          alert('Login successful');
      } catch (error) {
        this.error = 'Invalid credentials. Please try again.';
        console.error(error);
      }
    }
  }
});