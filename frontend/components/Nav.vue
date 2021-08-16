<template>
  <nav id="mainNav" class="navbar navbar-expand-lg navbar-light fixed-top">
    <div class="container">
      <NuxtLink class="navbar-brand" :to="{ name: 'index' }">
        Start Bootstrap
      </NuxtLink>
      <button
        class="navbar-toggler navbar-toggler-right"
        type="button"
        data-toggle="collapse"
        data-target="#navbarResponsive"
        aria-controls="navbarResponsive"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        Menu
        <i class="fas fa-bars" />
      </button>
      <div id="navbarResponsive" class="collapse navbar-collapse">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item">
            <NuxtLink class="nav-link" :to="{ name: 'index' }">
              Home
            </NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink class="nav-link" :to="{ name: 'about' }">
              About
            </NuxtLink>
          </li>

          <li class="nav-item">
            <NuxtLink class="nav-link" :to="{ name: 'create' }">
              Sample Post
            </NuxtLink>
          </li>

          <li v-if="!$auth.loggedIn" class="nav-item">
            <NuxtLink class="nav-link" :to="{ name: 'login' }">
              Login
            </NuxtLink>
          </li>
          <li v-if="$auth.loggedIn" class="nav-item" @click.prevent="logout">
            <a class="nav-link" href="#"> Logout </a>
          </li>
          <li v-if="$auth.loggedIn" class="nav-item">
            <NuxtLink class="nav-link" :to="{ name: 'profile' }">
              Profile
            </NuxtLink>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  methods: {
    async logout () {
      await this.$auth.logout()
    }
  }
}
</script>
