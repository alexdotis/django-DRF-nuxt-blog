<template>
  <div>
    <Header
      title="Login"
      subheading="Login and write your article"
      image="img/contact-bg.jpg"
    />

    <Form
      :schema="schema"
      :buttonschema="buttonSchema"
      :errors="errors"
      :slots="slots"
      @submit="login"
      @formdata="parseFormData"
    >
      <NuxtLink
        :slot="slots.slotNames"
        class="register"
        :to="{ name: 'register' }"
      >
        Register now
      </NuxtLink>

      <NuxtLink
        :slot="slots.slotNames"
        class="register-meta"
        :to="{ name: 'recover' }"
      >
        Forgot Password ?
      </NuxtLink>
    </Form>
  </div>
</template>

<script>
export default {
  middleware: ['auth'],
  data () {
    return {
      username: '',
      password: '',
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
            label: 'Password',
            type: 'password',
            name: 'password',
            placeholder: 'Password',
            required: true
          }
        ]
      },
      buttonSchema: {
        className: 'btn btn-primary',
        type: 'submit',
        name: 'Login'
      },
      slots: {
        slotNames: [
          {
            name: 'url'
          },
          {
            name: 'forgotpass'
          }
        ]
      }
    }
  },
  head: {
    title: 'Login',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      {
        hid: 'description',
        name: 'description',
        content: 'Login and write article!!'
      }
    ]
  },

  methods: {

    async login () {
      try {
        await this.$auth
          .loginWith('local', {
            data: {
              username: this.username,
              password: this.password
            }
          })
          .then(() => {
            this.$router.push('/')
          })
      } catch (error) {
        this.errors = error.response.data
      }
    },
    parseFormData (value, name) {
      if (name === 'username') {
        this.username = value
      }
      if (name === 'password') {
        this.password = value
      }
      this.errors = null
    }
  }
}
</script>

<style scoped>
.register {
  font-size: 13px;
  border-style: groove;
  border-radius: 20px;
  padding: 10px;
  border-width: 1px;
}
.register-meta {
  font-size: 13px;
  margin-left: 25px;
  border-style: groove;
  border-radius: 20px;
  padding: 10px;
  border-width: 1px;
}
</style>
