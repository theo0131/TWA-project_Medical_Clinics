<template>
  <div id="app">
    <h1>Users</h1>
    <ul>
      <li v-for="(user, index) in users" :key="index">{{ user.name }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
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

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
