<template>
  <div>
    <Header
      title="Recover Password"
      subheading="Let us help you to recover your password"
      image="img/contact-bg.jpg"
    />
    <Form
      :schema="schema"
      :buttonschema="buttonSchema"
      :errors="errors"
      :success="success"
      @submit="recover"
      @formdata="parseFormData"
    />
  </div>
</template>

<script>
export default {
  data () {
    return {
      email: '',
      errors: null,
      success: null,
      schema: {
        fields: [
          {
            label: 'email',
            name: 'email',
            placeholder: 'Email',
            type: 'text',
            required: true
          }
        ]
      },
      buttonSchema: {
        name: 'Send',
        type: 'submit',
        className: 'btn btn-primary'
      }
    }
  },
  head () {
    return {
      title: 'Recover Password'
    }
  },
  created () {
    if (this.$auth.loggedIn) {
      this.$router.push('/')
    }
  },
  methods: {
    async recover () {
      try {
        await this.$axios
          .post('rest-auth/password/reset/', {
            email: this.email
          })
          .then((resp) => {
            this.success = resp.data.detail
          })
      } catch (error) {
        this.errors = error.response.data
      }
    },
    parseFormData (value, name) {
      if (name === 'email') {
        this.email = value
      }
      this.errors = null
    }
  }
}
</script>
