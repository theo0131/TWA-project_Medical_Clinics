<template>
    <router-view></router-view>
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
  