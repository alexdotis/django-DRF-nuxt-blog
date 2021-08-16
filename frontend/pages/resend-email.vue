<template>
  <div>
    <Header title="Resend email" subheading="Please verify your email" />
    <Form
      :schema="schema"
      :buttonschema="buttonSchema"
      :errors="errors"
      :success="success"
      @submit="resendEmail"
      @formdata="parseFormData"
    />
  </div>
</template>

<script>
export default {
  middleware: ['verification'],
  data () {
    return {
      errors: null,
      success: null,

      schema: {
        fields: [
          {
            label: 'Email',
            placeholder: 'Email',
            name: 'email',
            required: true,
            type: 'text'
          }
        ]
      },
      buttonSchema: {
        name: 'Send',
        className: 'btn btn-success'
      }
    }
  },
  head () {
    return {
      title: 'Resend Email'
    }
  },
  methods: {
    async resendEmail () {
      try {
        await this.$axios
          .post('rest-auth/registration/resend-email/', {
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
