<template>
  <div>
    <Header
      title="Reset Password"
      subheading="Reset password confirmed ?"
      image="img/contact-bg.jpg"
    />
    <Form
      :schema="schema"
      :buttonschema="buttonSchema"
      :errors="errors"
      @submit="resetPassword"
      @formdata="formdata"
    />
  </div>
</template>

<script>
export default {
  /* eslint-disable no-console */
  data () {
    return {
      uid: '',
      token: '',
      password1: '',
      password2: '',
      errors: null,
      schema: {
        fields: [
          {
            label: 'New Password1',
            type: 'password',
            name: 'new_password1',
            placeholder: 'New Password 1',
            required: true
          },
          {
            label: 'New Password2',
            type: 'password',
            placeholder: 'New Password 2',
            required: true,
            name: 'new_password2'
          }
        ]
      },
      buttonSchema: {
        className: 'btn btn-primary',
        name: 'Submit',
        type: 'submit'
      }
    }
  },
  head () {
    return {
      title: 'Password Reset'
    }
  },
  created () {
    const params = this.$route.params
    this.uid = params.uid
    this.token = params.token
  },
  methods: {
    async resetPassword () {
      try {
        await this.$axios
          .post('rest-auth/password/reset/confirm/', {
            new_password1: this.password1,
            new_password2: this.password2,
            uid: this.uid,
            token: this.token
          })
          .then((resp) => {
            alert(resp.data.detail)
            this.$router.push('/login')
          })
      } catch (error) {
        this.errors = error.response.data
      }
    },
    formdata (value, name) {
      if (name === 'new_password1') {
        this.password1 = value
      }
      if (name === 'new_password2') {
        this.password2 = value
      }
      this.errors = null
    }
  }
}
</script>
