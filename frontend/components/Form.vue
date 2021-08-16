<template>
  <div class="container">
    <div class="row">
      <div class="col-lg-8 col-md-10 mx-auto">
        <form @submit.prevent="submitForm">
          <div
            v-for="(field, index) in schema.fields"
            :key="index"
            class="control-group"
          >
            <div class="form-group floating-label-form-group controls">
              <label>{{ field.label }}</label>
              <input
                :value="field.value"
                :name="field.name"
                :type="field.type"
                :placeholder="field.placeholder"
                :required="field.required"
                class="form-control"
                @input="formdata($event.target.value, field.name)"
              >
            </div>
          </div>
          <br>

          <div
            v-for="slotname in slots"
            :key="slotname.name"
            class="control-group"
          >
            <slot :name="slotname" />
          </div>

          <br>

          <button :type="buttonschema.type" :class="buttonschema.className">
            {{ buttonschema.name }}
          </button>
          <div v-if="errorMessages.length > 0" class="errorclass">
            <div
              v-for="msg in errorMessages"
              :key="msg"
              class="alert alert-danger"
              role="alert"
            >
              {{ msg }}
              <li v-if="msg.includes('E-mail is not verified.')">
                <NuxtLink :to="{ name: 'resend-email' }">
                  Resend Email
                </NuxtLink>
              </li>
            </div>
          </div>
          <div v-if="success" class="alert alert-success" role="alert">
            {{ success }}
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    schema: {
      type: Object,
      default: () => ({}),
      required: true
    },
    buttonschema: {
      type: Object,
      default: () => ({}),
      required: true
    },
    errors: {
      type: [Object, Array],
      default: () => null

    },
    success: {
      type: String,
      default: null,
      required: false
    },

    slots: {
      type: Object,
      default: () => null,
      required: false
    }
  },
  data () {
    return {
      formErrors: []
    }
  },

  computed: {
    errorMessages () {
      if (this.errors != null) {
        for (const item in this.errors) {
          if (typeof this.errors[item] === 'string') {
            continue
          } else {
            this.errors[item].forEach((element) => {
              this.formErrors.push(element)
            })
          }
        }
        return this.formErrors.length > 0 ? this.formErrors : this.errors
      }
      return this.formErrors
    }
  },

  methods: {
    submitForm () {
      this.$emit('submit')
      this.formErrors = []
    },
    formdata (value, fieldName) {
      this.$emit('formdata', value, fieldName)
    }
  }
}
</script>
