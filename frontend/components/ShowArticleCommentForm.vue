<template>
  <div class="container" style="margin-top: 50px">
    <div class="row">
      <div class="col-lg-8 col-md-10 mx-auto">
        <form v-show="isAuthenticated" @submit.prevent="postComment">
          <div class="control-group">
            <div class="form-group floating-label-form-group controls">
              <label>Comment</label>
              <input
                id="comment"
                v-model="comment"
                type="text"
                class="form-control"
                placeholder="Leave your comment"
                required
              >
              <p class="help-block text-danger" />
            </div>
          </div>

          <br>
          <button type="submit" class="btn btn-primary">
            Post Comment
          </button>
        </form>
        <div v-show="!isAuthenticated">
          <p>
            Please <NuxtLink :to="{ name: 'login' }">
              Log in
            </NuxtLink> to
            leave a comment
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      isAuthenticated: false,
      comment: ''
    }
  },
  mounted () {
    /* eslint-disable no-console */
    if (this.$auth.loggedIn) {
      this.isAuthenticated = !this.isAuthenticated
    }
  },
  methods: {
    async postComment () {
      const slug = this.$route.params.slug
      await this.$axios
        .post(`api/comment/${slug}/create/`, {
          comment_text: this.comment
        })
        .then(() => {
          this.$store.dispatch('ArticleDetailView', { slug })
        })
      this.comment = ''
    }
  }
}
</script>
