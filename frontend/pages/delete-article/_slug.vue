<template>
  <div>
    <Header title="Delete Article" subheading="Delete your article?" />
    <button class="btn btn-success" @click.prevent="deleteArticle">
      Delete
    </button>
    <button class="btn btn-warning" @click.prevent="goBack">
      No
    </button>
  </div>
</template>

<script>
export default {
  methods: {
    async deleteArticle () {
      try {
        await this.$axios
          .delete(`api/article/${this.$route.params.slug}/delete/`)
          .then(() => {
            alert('article successfully deleted')
            this.$router.push('/')
          })
      } catch (error) {
        alert(error.response.data)
      }
    },
    goBack () {
      this.$router.push('/')
    }
  }
}
</script>
