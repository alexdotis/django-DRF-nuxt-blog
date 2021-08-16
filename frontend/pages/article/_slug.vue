<template>
  <div>
    <Header
      :title="object.title"
      :subheading="object.subheading"
      :image="object.image"
    />
    <div class="container">
      <div class="row">
        <!-- eslint-disable vue/no-v-html -->
        <div class="col-lg-8 col-md-10 mx-auto" v-html="object.text" />
      </div>
    </div>

    <div v-if="userIsAuthor">
      <NuxtLink
        class="update"
        :to="{
          name: 'update-article-slug',
          params: { slug: $route.params.slug },
        }"
      >
        Update
      </NuxtLink>
      <NuxtLink
        class="delete"
        :to="{
          name: 'delete-article-slug',
          params: { slug: $route.params.slug },
        }"
      >
        Delete
      </NuxtLink>
    </div>

    <hr>

    <div class="container" style="margin-top: 50px">
      <div class="row">
        <div class="col-lg-8 col-md-10 mx-auto">
          <h4 class="post-meta far fa-comment">
            {{ object.total_comments }}
          </h4>

          <button
            :disabled="buttonToggle"
            type="button"
            class="btn btn-default"
            style="padding: 0px"
            :style="articleReview(object.pk) === 'Like' ? 'color:blue' : null"
            @click.prevent="articleLike(object.pk)"
          >
            <i
              class="far fa-thumbs-up"
              style="font-size: 25px; padding-left: 20px; padding-bottom: 11px"
            >
              {{ object.total_likes }}
            </i>
          </button>
          <button
            :disabled="buttonToggle"
            type="button"
            class="btn btn-default"
            style="padding-left: 20px; padding-bottom: 11px"
            :style="articleReview(object.pk) === 'Dislike' ? 'color:red' : null"
            @click.prevent="articleDislike(object.pk)"
          >
            <i
              class="far fa-thumbs-down"
              style="font-size: 25px; padding-left: 10px; padding-bottom: 11px"
            >
              {{ object.total_dislikes }}</i>
          </button>

          <hr>

          <ShowArticleComments :button-toggle="buttonToggle" />
        </div>
      </div>

      <ShowArticleCommentForm />
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
export default {
  data () {
    return {
      UserComment: '',
      commentsToShow: 4,
      userIsAuthor: false,
      buttonToggle: true
    }
  },
  async fetch ({ store, error, params }) {
    try {
      await store.dispatch('ArticleDetailView', { slug: params.slug })
    } catch (e) {
      error({ statusCode: 404, message: 'Not Found' })
    }
  },
  head () {
    return {
      title: this.object.title,
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          hid: 'description',
          name: 'description',
          content: this.object.title
        }
      ]
    }
  },
  computed: {
    object () {
      return this.$store.state.articleDetailData
    }
  },
  created () {
    if (this.$auth.loggedIn) {
      this.buttonToggle = !this.buttonToggle
    }
    this.userCanUpdateArticle()
  },
  methods: {
    ...mapActions({
      likeArticle: 'ArticleLike',
      dislikeArticle: 'ArticleDislike',
      dispatchArticle: 'ArticleDetailView',
      voteSystem: 'VoteSystem'
    }),
    articleReview (objectId) {
      const ArticleReviewData = this.$store.state.userVoteSystem

      return ArticleReviewData.map((obj) => {
        if (
          obj.content_type.includes('article') &&
          obj.object_id === objectId
        ) {
          return obj.vote
        } else {
          return false
        }
      })
        .filter(e => e !== false)
        .join(' ')
    },

    async articleLike (articlePk) {
      await this.likeArticle({ pk: articlePk })
      await this.voteSystem()
      await this.dispatchArticle({ slug: this.$route.params.slug })
    },
    async articleDislike (articlePk) {
      await this.dislikeArticle({ pk: articlePk })
      await this.voteSystem()
      await this.dispatchArticle({ slug: this.$route.params.slug })
    },
    userCanUpdateArticle () {
      if (this.$auth.loggedIn && this.$auth.user === this.object.author) {
        this.userIsAuthor = !this.userIsAuthor
      }
    }
  }
}
</script>

<style scoped>
.update {
  font-size: 15px;
  border-style: groove;
  border-radius: 20px;
  padding: 10px;
  border-width: 1px;
}
.delete {

    font-size: 15px;
    border-style: groove;
    border-radius: 20px;
    padding: 10px;
    border-width: 1px;

}
</style>
