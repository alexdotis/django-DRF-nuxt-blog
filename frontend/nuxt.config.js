export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'frontend',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' }
    ],
    link: [
      { rel: 'stylesheet', type: 'text/css', href: 'https://fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic' },
      { rel: 'stylesheet', type: 'text/css', href: '/vendor/fontawesome-free/css/all.min.css' },
      { rel: 'stylesheet', href: '/vendor/bootstrap/css/bootstrap.min.css' },
      { rel: 'stylesheet', href: '/css/clean-blog.min.css' },
      { rel: 'stylesheet', type: 'text/css', href: 'https://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800' },

    ],
    script: [
      { src: '/vendor/jquery/jquery.min.js', body: true },
      { src: '/vendor/bootstrap/js/bootstrap.bundle.min.js', body: true },
      { src: '/js/clean-blog.min.js', body: true }

    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
    // '@static/vendor/bootstrap/css/bootstrap.min.css',
    // '@static/vendor/fontawesome-free/css/all.min.css',
    // '@static/css/clean-blog.min.css'
    
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/eslint
    '@nuxtjs/eslint-module'
  ], eslint: {
    fix: true
  },

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    '@nuxtjs/auth-next'
  ],

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    baseURL: 'http://127.0.0.1:8000',
    // plugins: ['~/plugins/axios.js'],

  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
  },
  auth: {
    strategies: {
        local: {
          user: {
            property: 'username',
            autoFetch: true
          },

          endpoints: {

            login: { url: '/rest-auth/login/', method: 'post' },
            logout: { url: '/rest-auth/logout/', method: 'post' },
            user: { url: '/rest-auth/user/', method: 'get' },
          },
          token:{
          property: 'key',
          type: 'Token',
          name:'Authorization'
          
          }
        }
      }
    }
  }
