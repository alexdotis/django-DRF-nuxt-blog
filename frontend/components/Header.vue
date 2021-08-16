<template>
  <header class="masthead" :style="{backgroundImage: `url(${image})`}">
    <div class="overlay" />
    <div class="container">
      <div class="row">
        <div class="col-lg-8 col-md-10 mx-auto">
          <div class="site-heading">
            <h1>{{ title }}</h1>
            <span class="subheading">{{ subheading }}</span>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: 'title'
    },
    subheading: {
      type: String,
      default: 'subheading'
    },
    image: {
      type: String,
      default: '/img/home-bg.jpg'
    }

  }
}
</script>
