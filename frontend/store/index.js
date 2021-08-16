
import {
  DETAIL_BEGIN,
  DETAIL_FAILURE,
  DETAIL_SUCCESS,
  COMMENT_BEGIN,
  COMMENT_SUCCESS,
  COMMENT_FAILURE,
  LIKE_ARTICLE_BEGIN,
  LIKE_ARTICLE_SUCCESS,
  LIKE_ARTICLE_FAILURE,
  DISLIKE_ARTICLE_BEGIN,
  DISLIKE_ARTICLE_SUCCESS,
  DISLIKE_ARTICLE_FAILURE,
  LIKE_COMMENT_BEGIN,
  LIKE_COMMENT_SUCCESS,
  LIKE_COMMENT_FAILURE,
  DISLIKE_COMMENT_BEGIN,
  DISLIKE_COMMENT_SUCCESS,
  DISLIKE_COMMENT_FAILURE,
  USER_VOTESYSTEM_BEGIN,
  USER_VOTESYSTEM_SUCCESS,
  USER_VOTESYSTEM_FAILURE
} from './api/types.js'

export const state = () => ({
  error: null,
  loading: false,
  articleDetailData: [],
  userVoteSystem: []

})

export const getters = {
  commentsLength (state) {
    return state.articleDetailData.comments.length
  },
  commentList (state) {
    return state.articleDetailData.comments
  }

}

export const mutations = {

  [DETAIL_BEGIN] (state) {
    this.state.loading = true
    this.state.error = false
  },
  [DETAIL_SUCCESS] (state, data) {
    this.state.loading = false
    this.state.error = false
    this.state.articleDetailData = data
  },
  [DETAIL_FAILURE] (state) {
    this.state.loading = false
    this.state.error = true
  },
  [COMMENT_BEGIN] (state) {
    this.state.loading = true
    this.state.error = false
  },
  [COMMENT_SUCCESS] (state) {
    this.state.loading = false
    this.state.error = true
  },
  [COMMENT_FAILURE] (state) {
    this.state.loading = false
    this.state.error = true
  },
  [LIKE_ARTICLE_BEGIN] (state) {
    this.state.loading = true
    this.state.error = false
  },
  [LIKE_ARTICLE_SUCCESS] (state) {
    this.state.loading = false
    this.state.error = false
  },
  [LIKE_ARTICLE_FAILURE] (state) {
    this.state.loading = false
    this.state.error = true
  },
  [DISLIKE_ARTICLE_BEGIN] (state) {
    this.state.loading = false
    this.state.error = true
  },
  [DISLIKE_ARTICLE_SUCCESS] (state) {
    this.state.loading = false
    this.state.error = false
  },
  [DISLIKE_ARTICLE_FAILURE] (state) {
    this.state.loading = false
    this.state.error = true
  },
  [LIKE_COMMENT_BEGIN] (state) {
    this.state.loading = true
    this.state.error = false
  },
  [LIKE_COMMENT_SUCCESS] (state) {
    this.state.loading = false
    this.state.error = false
  },
  [LIKE_COMMENT_FAILURE] (state) {
    this.state.loading = false
    this.state.error = true
  },
  [DISLIKE_COMMENT_BEGIN] (state) {
    this.state.loading = true
    this.state.error = false
  },
  [DISLIKE_COMMENT_SUCCESS] (state) {
    this.state.loading = false
    this.state.error = false
  },
  [DISLIKE_COMMENT_FAILURE] (state) {
    this.state.loading = false
    this.state.error = true
  },

  [USER_VOTESYSTEM_BEGIN] (state) {
    this.state.loading = true
    this.state.error = false
  },
  [USER_VOTESYSTEM_SUCCESS] (state, data) {
    this.state.loading = false
    this.state.error = false
    this.state.userVoteSystem = data
  },
  [USER_VOTESYSTEM_FAILURE] (state) {
    this.state.loading = false
    this.state.error = true
    this.state.userVoteSystem = []
  }
}

export const actions = {

  async VoteSystem ({ commit }) {
    commit(USER_VOTESYSTEM_BEGIN)
    return await this.$axios.get('api/vt/')
      .then(({ data }) => commit(USER_VOTESYSTEM_SUCCESS, data))
  },

  async ArticleDetailView ({ commit }, { slug }) {
    commit(DETAIL_BEGIN)
    return await this.$axios.get(`api/article/${slug}/`)
      .then(({ data }) => commit(DETAIL_SUCCESS, data))
  },

  async ArticleLike ({ commit }, { pk }) {
    commit(LIKE_ARTICLE_BEGIN)
    return await this.$axios.post(`api/article/${pk}/like`)
      .then(() => commit(LIKE_ARTICLE_SUCCESS))
      .catch(() => commit(LIKE_ARTICLE_FAILURE))
  },

  async ArticleDislike ({ commit }, { pk }) {
    commit(DISLIKE_ARTICLE_BEGIN)
    return await this.$axios.post(`api/article/${pk}/dislike`)
      .then(() => commit(DISLIKE_ARTICLE_SUCCESS))
      .catch(() => commit(DISLIKE_ARTICLE_FAILURE))
  },
  async commentLike ({ commit }, { pk }) {
    commit(LIKE_COMMENT_BEGIN)
    return await this.$axios.post(`api/comment/${pk}/like`)
      .then(() => commit(LIKE_COMMENT_SUCCESS))
      .catch(() => commit(LIKE_COMMENT_FAILURE))
  },
  async commentDislike ({ commit }, { pk }) {
    commit(DISLIKE_COMMENT_BEGIN)
    return await this.$axios.post(`api/comment/${pk}/dislike`)
      .then(() => commit(DISLIKE_COMMENT_SUCCESS))
      .catch(() => commit(DISLIKE_COMMENT_FAILURE))
  }

}
