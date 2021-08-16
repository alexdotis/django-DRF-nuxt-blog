<template>
  <div>
    <Header
      title="Register"
      subheading="Register now!"
      image="img/contact-bg.jpg"
    />
    <Form
      :schema="schema"
      :buttonschema="buttonSchema"
      :errors="errors"
      @formdata="parseFormData"
      @submit="registerUser"
    />
  </div>
</template>

<script>
export default {
  data () {
    return {
      username: '',
      email: '',
      password1: '',
      password2: '',
      errors: null,
      schema: {
        fields: [
          {
            label: 'Username',
            type: 'text',
            name: 'username',
            placeholder: 'Username',
            required: true
          },
          {
            label: 'email',
            type: 'text',
            name: 'email',
            placeholder: 'Email',
            required: true
          },
          {
            label: 'Password1',
            type: 'password',
            name: 'password1',
            placeholder: 'Password 1',
            required: true
          },
          {
            label: 'Password2',
            type: 'password',
            name: 'password2',
            placeholder: 'Password 2',
            required: true
          }
        ]
      },
      buttonSchema: {
        className: 'btn btn-primary',
        type: 'submit',
        name: 'Register'
      }
    }
  },
  head () {
    return {
      title: 'Register'
    }
  },
  created () {
    if (this.$auth.loggedIn) {
      this.$router.push('/')
    }
  },
  methods: {
    async registerUser () {
      try {
        await this.$axios
          .post('rest-auth/registration/', {
            username: this.username,
            email: this.email,
            password1: this.password1,
            password2: this.password2
          })
          .then(() => {
            // instead of alert some modal here
            alert('Check your email for verification')
            this.$router.push({ name: 'login' })
          })
      } catch (error) {
        this.errors = error.response.data
      }
    },

    parseFormData (value, name) {
      if (name === 'email') {
        this.email = value
      }
      if (name === 'username') {
        this.username = value
      }
      if (name === 'password1') {
        this.password1 = value
      }
      if (name === 'password2') {
        this.password2 = value
      }
      this.errors = null
    }
  }
}
</script>
