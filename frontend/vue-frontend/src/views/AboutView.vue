<template>
  <div>
    <NavBar></NavBar>
    <h1>This is a div used specifically to check CRUD operations, specifically Read</h1>
    <h2>Users</h2>
    <ul>
      <li v-for="(user, index) in users" :key="index">{{ user.name }}</li>
    </ul>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'

export default {
  name: 'HomeView',
  components:{
    NavBar
  },
  data() {
    return {
      users: [],
    };
  },
  mounted() {
    fetch('http://localhost:5000/api/users')
      .then(response => response.json())
      .then(data => {
        this.users = data;
      });
  },
};
</script>

<style scoped>
</style>
