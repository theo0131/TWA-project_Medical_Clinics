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
    name: 'AppointmentsHome',
    data() {
      return {
        users: [],
      };
    },
    mounted() {
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
  