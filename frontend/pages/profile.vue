<template>
  <div>
    <Header title="Your profile" subheading="Change your profile" />
    <Form
      :schema="schema"
      :buttonschema="buttonSchema"
      :errors="errors"
      :slots="slots"
      :success="success"
      @submit="updateUser"
      @formdata="parseFormData"
    >
      <NuxtLink
        :slot="slots.slotNames"
        class="nuxt-page"
        :to="{ name: 'change-password' }"
      >
        Change password
      </NuxtLink>
    </Form>
  </div>
</template>

<script>
export default {
  middleware: ['authenticated'],
  data () {
    return {
      username: '',
      firstname: '',
      lastname: '',
      errors: null,
      success: '',
      schema: {
        fields: [
          {
            label: 'Username',
            name: 'username',
            type: 'text',
            placeholder: 'Username',
            required: true,
            value: ''
          },
          {
            label: 'First Name',
            name: 'firstname',
            type: 'text',
            placeholder: 'First Name',
            required: false,
            value: ''
          },
          {
            label: 'Last Name',
            name: 'lastname',
            type: 'text',
            placeholder: 'Last Name',
            required: false,
            value: ''
          }
        ]
      },
      buttonSchema: {
        className: 'btn btn-primary',
        type: 'submit',
        name: 'Update'
      },
      slots: {
        slotNames: [
          {
            name: 'change'
          }
        ]
      }
    }
  },
  head () {
    return {
      title: 'User Profile'
    }
  },

  created () {
    this.userData()
  },
  methods: {
    async updateUser () {
      try {
        await this.$axios
          .put('rest-auth/user/', {
            username: this.username,
            first_name: this.firstname,
            last_name: this.lastname
          })
          .then(() => {
            this.success = 'User Updated'
          })
      } catch (error) {
        this.errors = error.response.data
      }
      this.userData()
    },
    async userData () {
      try {
        await this.$axios.get('rest-auth/user/').then((resp) => {
          this.username = resp.data.username
          this.firstname = resp.data.first_name
          this.lastname = resp.data.last_name
        })
        this.$auth.setUser(this.username)
        this.schema.fields[0].value = this.username
        this.schema.fields[1].value = this.firstname
        this.schema.fields[2].value = this.lastname
      } catch (error) {
        this.errors = error.response.data
      }
    },
    parseFormData (value, name) {
      if (name === 'username') {
        this.username = value
      }
      if (name === 'firstname') {
        this.firstname = value
      }
      if (name === 'lastname') {
        this.lastname = value
      }
      this.errors = null
    }
  }
}
</script>

<style scoped>
.nuxt-page {
  font-size: 13px;
  border-style: groove;
  border-radius: 20px;
  padding: 10px;
  border-width: 1px;
}
</style>
