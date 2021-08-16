<template>
  <div>
    <h1>Verification Email</h1>
  </div>
</template>

<script>
export default {
  data () {
    return {
      key: null
    }
  },
  head () {
    return {
      title: 'Verification Email'
    }
  },
  created () {
    this.key = this.$route.params.key
    this.confirmationEmail()
  },
  methods: {
    async confirmationEmail () {
      try {
        await this.$axios
          .post('rest-auth/account-confirm-email/', {
            key: this.key
          })
          .then(() => {
            alert('Your email successfully confirmed!')
            this.$router.push({ name: 'login' })
          })
      } catch (error) {
        alert(`${error.response.data.detail} Please Check again your url`)
        this.$router.push({ name: 'resend-email' })
      }
    }
  }
}
</script>
