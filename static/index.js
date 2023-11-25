new Vue({
  el: '#app',
  methods: {
    goTo(path) {
      window.location.href = path;
    }
  }
});