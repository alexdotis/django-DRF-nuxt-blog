<template>
  <div>
    <Header title="Post Your article" subheading="Time to post your article" />
    <Form
      v-show="isAuthenticated"
      :schema="schema"
      :buttonschema="buttonSchema"
      :slots="slots"
      :errors="errors"
      @submit="submitForm"
      @formdata="parseFormData"
    >
      <div :slot="slots.slotNames" class="control-group">
        <div class="form-group floating-label-form-group controls">
          <label>Message</label>
          <textarea
            id="id_text"
            cols="40"
            name="text"
            rows="10"
            required
            data-processed="0"
            data-external-plugin-resources="[]"
            data-id="id_text"
            data-type="ckeditortype"
            :data-config="dataConfig"
          />
        </div>
      </div>
      <div :slot="slots.slotNames" class="control-group">
        <div class="form-group floating-label-form-group controls">
          <label>Image</label>
          <input
            ref="file"
            type="file"
            accept="image/png, image/jpeg, image/bmp"
            class="form-control"
            placeholder="Title"
            required="true"
            data-validation-required-message="Please enter your name."
          >
          <p class="help-block text-danger" />
        </div>
      </div>
    </Form>
    <div v-if="!isAuthenticated" class="container">
      <div class="row">
        <div class="col-lg-8 col-md-10 mx-auto">
          <div class="control-group">
            <div class="form-group floating-label-form-group controls">
              <h5>
                Please -
                <NuxtLink
                  :to="{ name: 'login' }"
                  style="border-style: groove; padding: 5px; border-width: 1px"
                >
                  Login
                </NuxtLink>
                - To post your article
              </h5>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      dataConfig:
        // '{"skin": "moono-lisa", "toolbar_Basic": [["Source", "-", "Bold", "Italic"]], "toolbar_Full": [["Styles", "Format", "Bold", "Italic", "Underline", "Strike", "SpellChecker", "Undo", "Redo"], ["Link", "Unlink", "Anchor"], ["Image", "Flash", "Table", "HorizontalRule"], ["TextColor", "BGColor"], ["Smiley", "SpecialChar"], ["Source"]], "toolbar": "Full", "height": 291, "width": 835, "filebrowserWindowWidth": 940, "filebrowserWindowHeight": 725, "removePlugins": "stylesheetparser", "allowedContent": true, "extraAllowedContent": "*(*)", "filebrowserUploadUrl": "http://127.0.0.1:8000/api/image/upload/", "filebrowserBrowseUrl": "http://127.0.0.1:8000/ckeditor/browse/", "language": "en-us"}',
        '{"skin": "moono-lisa", "toolbar_Basic": [["Source", "-", "Bold", "Italic"]], "toolbar_Full": [["Styles", "Format", "Bold", "Italic", "Underline", "Strike", "SpellChecker", "Undo", "Redo"], ["Link", "Unlink", "Anchor"], ["Image", "Flash", "Table", "HorizontalRule"], ["TextColor", "BGColor"], ["Smiley", "SpecialChar"], ["Source"]], "toolbar": "YourCustomToolbarConfig", "height": 291, "width": 835, "filebrowserWindowWidth": 940, "filebrowserWindowHeight": 725, "toolbar_YourCustomToolbarConfig": [{"name": "clipboard", "items": ["Undo", "Redo"]}, {"name": "basicstyles", "items": ["Bold", "Italic", "Underline"]}, {"name": "paragraph", "items": ["NumberedList", "BulletedList", "-", "Outdent", "Indent", "-", "Blockquote", "-", "JustifyLeft", "JustifyCenter", "JustifyRight", "JustifyBlock", "-", "BidiLtr", "BidiRtl"]}, {"name": "links", "items": ["Link", "Unlink"]}, {"name": "insert", "items": ["Image", "Flash", "Table", "HorizontalRule", "Smiley", "SpecialChar", "PageBreak"]}, "/", {"name": "styles", "items": ["Styles", "Format", "Font", "FontSize"]}, {"name": "colors", "items": ["TextColor", "BGColor"]}, {"name": "tools", "items": ["Maximize", "ShowBlocks"]}, "/", {"name": "yourcustomtools", "items": ["Preview", "Maximize"]}], "tabSpaces": 4, "extraPlugins": "uploadimage,div,autolink,autoembed,embedsemantic,autogrow,widget,lineutils,clipboard,dialog,dialogui,elementspath", "filebrowserUploadUrl": "http://127.0.0.1:8000/api/image/upload/", "filebrowserBrowseUrl": "http://127.0.0.1:8000/ckeditor/browse/", "language": "en-us"}',

      title: '',
      subheading: '',
      errors: null,
      isAuthenticated: false,
      schema: {
        fields: [
          {
            label: 'Title',
            name: 'title',
            type: 'text',
            required: true,
            placeholder: 'Title'
          },
          {
            label: 'Subheading',
            name: 'subheading',
            type: 'text',
            required: true,
            placeholder: 'Subheading'
          }
        ]
      },
      buttonSchema: {
        type: 'submit',
        className: 'btn btn-primary',
        name: 'Create'
      },
      slots: {
        slotNames: [
          {
            name: 'editor'
          },
          {
            name: 'file'
          }
        ]
      }
    }
  },
  head () {
    return {
      title: 'Create Article',
      script: [
        { src: 'http://127.0.0.1:8000/static/ckeditor/ckeditor-init.js' },
        { src: 'http://127.0.0.1:8000/static/ckeditor/ckeditor/ckeditor.js' }
      ]
    }
  },
  created () {
    if (this.$auth.loggedIn) {
      this.isAuthenticated = !this.isAuthenticated
    }
  },
  /* eslint-disable no-console */
  methods: {
    async submitForm () {
      if (window.CKEDITOR.instances.id_text.getData().length === 0) {
        alert('Text required')
      } else {
        const form = new FormData()
        form.append('title', this.title)
        form.append('subheading', this.subheading)
        form.append('text', window.CKEDITOR.instances.id_text.getData())
        form.append('image', this.$refs.file.files[0])
        try {
          await this.$axios
            .post('api/article/create/', form, {
              headers: { 'Content-Type': 'multipart/form-data' }
            })
            .then(() => {
              document.getElementById('id_text').value = null
              this.$refs.file.value = null
              this.$router.push('/')
            })
        } catch (error) {
          this.errors = error.response.data
        }
      }
    },
    parseFormData (value, name) {
      if (name === 'title') {
        this.title = value
      }
      if (name === 'subheading') {
        this.subheading = value
      }
      this.errors = null
    }
  }
}
</script>
