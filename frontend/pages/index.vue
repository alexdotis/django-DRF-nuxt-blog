<template>
  <div>
    <Header
      title="Welcome to my blog"
      subheading="Read the best articles"
      image="/img/home-bg.jpg"
    />
    <div class="container">
      <div class="row">
        <div class="col-lg-8 col-md-10 mx-auto">
          <div
            v-for="article in object_list.results"
            :key="article.pk"
            class="post-preview"
          >
            <NuxtLink
              :to="{ name: 'article-slug', params: { slug: article.slug } }"
            >
              <h2 class="post-title">
                {{ article.title }}
              </h2>
              <h3 class="post-subtitle">
                {{ article.subheading }}
              </h3>
            </NuxtLink>
            <p class="post-meta">
              Posted by
              <a href="#">{{ article.author }}</a>
              on {{ new Date(article.created_at).toDateString() }}
            </p>
            <p class="post-meta far fa-comment">
              {{ article.total_comments }}
            </p>
            <p class="post-meta far fa-thumbs-up" style="margin: 10px">
              {{ article.total_likes }}
            </p>
            <p class="post-meta far fa-thumbs-down">
              {{ article.total_dislikes }}
            </p>

            <hr>
          </div>
          <div class="clearfix">
            <!-- Pagination -->
            <nav aria-label="...">
              <ul v-if="object_list.links" class="pagination">
                <li v-if="object_list.links.previous" class="page-item">
                  <a
                    class="page-link"
                    type="button"
                    tabindex="-1"
                    @click.prevent="articleList(object_list.links.previous)"
                  >Previous</a>
                </li>
                <li v-if="object_list.links.previous" class="page-item">
                  <a
                    class="page-link"
                    type="button"
                    @click.prevent="articleList(object_list.links.previous)"
                  >{{ object_list.current_page - 1 }}</a>
                </li>
                <li class="page-item active">
                  <a
                    class="page-link"
                    type="button"
                  >{{ object_list.current_page }}
                    <span class="sr-only">(current)</span></a>
                </li>
                <li v-if="object_list.links.next" class="page-item">
                  <a
                    class="page-link"
                    type="button"
                    @click.prevent="articleList(object_list.links.next)"
                  >
                    {{ object_list.current_page + 1 }}
                  </a>
                </li>
                <li v-if="object_list.links.next" class="page-item">
                  <a
                    class="page-link"
                    type="button"
                    @click.prevent="articleList(object_list.links.next)"
                  >Next</a>
                </li>
              </ul>
            </nav>
          </div>
        </div>
      </div>
    </div>

    <hr>
  </div>
</template>

<script>
export default {
  data () {
    return {
      object_list: []
    }
  },
  head: {
    title: 'BlogSpot',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      {
        hid: 'description',
        name: 'description',
        content: 'All articles and some description'
      }
    ]
  },

  created () {
    this.articleList()
    if (this.$auth.loggedIn) {
      this.buttonToggle = !this.buttonToggle
      this.$store.dispatch('VoteSystem')
    } else {
      this.$store.commit('USER_VOTESYSTEM_FAILURE')
    }
  },

  methods: {
    async articleList (link) {
      if (link != null) {
        await this.fetchArticlesData(link)
      } else {
        const baseLink = 'api/articles/'
        await this.fetchArticlesData(baseLink)
      }
    },
    async fetchArticlesData (link) {
      await this.$axios.get(link).then((resp) => {
        this.object_list = resp.data
      })
    }
  }
}
</script>
