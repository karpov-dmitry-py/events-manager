<template>
  <div id="app">
    <div id="nav">
      <h1><router-link to="/">My Events</router-link></h1>
    </div>
    <router-view/>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 0px;
}

#nav a {
  font-weight: bold;
  color: darkgreen;
}

#nav a.router-link-exact-active {
  color: lightblue;
}
</style>
