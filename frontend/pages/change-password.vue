<template>
  <div>
    <Header
      title="Change Password"
      subheading="Change Password"
      image="img/contact-bg.jpg"
    />
    <Form
      :schema="schema"
      :buttonschema="buttonSchema"
      :errors="errors"
      @submit="changePassword"
      @formdata="parseFormData"
    />
  </div>
</template>

<script>
export default {
  middleware: ['authenticated'],
  data () {
    return {
      errors: null,
      password1: '',
      password2: '',

      schema: {
        fields: [
          {
            label: 'New Password 1',
            name: 'new_password1',
            type: 'password',
            placeholder: 'Password 1',
            required: true
          },

          {
            label: 'New Password 2',
            name: 'new_password2',
            type: 'password',
            placeholder: 'Password 2',
            required: true
          }
        ]
      },
      buttonSchema: {
        name: 'Change',
        className: 'btn btn-primary'
      }
    }
  },
  head () {
    return {
      title: 'Change Password'
    }
  },
  methods: {
    parseFormData (value, name) {
      if (name === 'new_password1') {
        this.password1 = value
      }
      if (name === 'new_password2') {
        this.password2 = value
      }
    },
    async changePassword () {
      try {
        await this.$axios
          .post('rest-auth/password/change/', {
            new_password1: this.password1,
            new_password2: this.password2
          })
          .then((resp) => {
            alert(resp.data.detail)
            this.$router.push({ name: 'profile' })
          })
      } catch (error) {
        this.errors = error.response.data
      }
    }
  }
}
</script>
