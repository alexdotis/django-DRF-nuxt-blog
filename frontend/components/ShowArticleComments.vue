<template>
  <div>
    <div v-for="comment in comments" :key="comment.id" class="post-preview">
      <p class="post-title">
        {{ comment.comment_text }}
      </p>
      <p class="post-meta">
        Posted by
        <a style="bold">{{ comment.user }}</a>
        on {{ new Date(comment.comment_created_at).toDateString() }}
      </p>
      <button
        :disabled="buttonToggle"
        type="button"
        class="btn btn-default"
        style="padding: 0px"
        :style="commentReview(comment.id) === 'Like' ? 'color:blue' : null"
        @click.prevent="LikeComment(comment.id)"
      >
        <i class="far fa-thumbs-up" style="font-size: 15px">
          {{ comment.total_likes }}</i>
      </button>
      <button
        :disabled="buttonToggle"
        type="button"
        class="btn btn-default"
        style="padding-left: 20px"
        :style="commentReview(comment.id) === 'Dislike' ? 'color:red' : null"
        @click.prevent="DislikeComment(comment.id)"
      >
        <i class="far fa-thumbs-down" style="font-size: 15px">
          {{ comment.total_dislikes }}</i>
      </button>
      <button
        v-if="comment.user === $auth.user"
        style="margin-left: 200px; font-size: 10px"
        class="btn btn-danger"
        @click.prevent="deleteCommentUser(comment.id)"
      >
        Delete
      </button>
      <hr>
    </div>

    <button
      v-if="commentsLength > 1"
      v-show="hasMoreComments"
      class="btn btn-primary"
      @click.prevent="loadMoreComments"
    >
      Load more
    </button>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
export default {
  props: {
    buttonToggle: {
      type: Boolean,
      required: true,
      default: true
    }
  },
  data () {
    return {
      commentsToShow: 3,
      hasMoreComments: true
    }
  },
  computed: {
    ...mapGetters(['commentsLength', 'commentList']),
    comments () {
      return this.commentList.slice(0, this.commentsToShow)
    }
  },
  methods: {
    ...mapActions({
      commentLike: 'commentLike',
      commentDislike: 'commentDislike',
      VoteSystem: 'VoteSystem',
      fetchArticle: 'ArticleDetailView'
    }),
    loadMoreComments () {
      this.commentsToShow += 3
      if (this.commentsLength === this.comments.length) {
        this.hasMoreComments = !this.hasMoreComments
      }
    },
    commentReview (commentId) {
      const CommentReviewData = this.$store.state.userVoteSystem
      return CommentReviewData.map((obj) => {
        if (
          obj.content_type.includes('comments') &&
          obj.object_id === commentId
        ) {
          return obj.vote
        } else {
          return false
        }
      })
        .filter(e => e !== false)
        .join(' ')
    },

    async LikeComment (commentId) {
      await this.commentLike({ pk: commentId })
      await this.VoteSystem()
      await this.fetchArticle({ slug: this.$route.params.slug })
    },
    async DislikeComment (commentId) {
      await this.commentDislike({ pk: commentId })
      await this.VoteSystem()
      await this.fetchArticle({ slug: this.$route.params.slug })
    },
    async deleteCommentUser (commentId) {
      try {
        await this.$axios
          .delete(`api/comment/${commentId}/delete/`)
          .then(() => {
            this.VoteSystem()
            this.fetchArticle({ slug: this.$route.params.slug })
          })
      } catch (error) {
        alert(error.response.data)
      }
    }
  }
}
</script>
