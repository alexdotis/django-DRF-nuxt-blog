<template>
  <div>
    <Header title="Update your article" subheading="Everything you need" />
    <Form
      :slots="slots"
      :schema="schema"
      :buttonschema="buttonSchema"
      :errors="errors"
      @formdata="parseFormData"
      @submit="articleUpdate"
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
          >
          <p class="help-block text-danger" />
        </div>
      </div>
    </Form>
  </div>
</template>

<script>
export default {
  middleware: ['authenticated'],
  data () {
    return {
      title: '',
      subheading: '',
      errors: null,
      dataConfig:
        '{"skin": "moono-lisa", "toolbar_Basic": [["Source", "-", "Bold", "Italic"]], "toolbar_Full": [["Styles", "Format", "Bold", "Italic", "Underline", "Strike", "SpellChecker", "Undo", "Redo"], ["Link", "Unlink", "Anchor"], ["Image", "Flash", "Table", "HorizontalRule"], ["TextColor", "BGColor"], ["Smiley", "SpecialChar"], ["Source"]], "toolbar": "YourCustomToolbarConfig", "height": 291, "width": 835, "filebrowserWindowWidth": 940, "filebrowserWindowHeight": 725, "toolbar_YourCustomToolbarConfig": [{"name": "clipboard", "items": ["Undo", "Redo"]}, {"name": "basicstyles", "items": ["Bold", "Italic", "Underline"]}, {"name": "paragraph", "items": ["NumberedList", "BulletedList", "-", "Outdent", "Indent", "-", "Blockquote", "-", "JustifyLeft", "JustifyCenter", "JustifyRight", "JustifyBlock", "-", "BidiLtr", "BidiRtl"]}, {"name": "links", "items": ["Link", "Unlink"]}, {"name": "insert", "items": ["Image", "Flash", "Table", "HorizontalRule", "Smiley", "SpecialChar", "PageBreak"]}, "/", {"name": "styles", "items": ["Styles", "Format", "Font", "FontSize"]}, {"name": "colors", "items": ["TextColor", "BGColor"]}, {"name": "tools", "items": ["Maximize", "ShowBlocks"]}, "/", {"name": "yourcustomtools", "items": ["Preview", "Maximize"]}], "tabSpaces": 4, "extraPlugins": "uploadimage,div,autolink,autoembed,embedsemantic,autogrow,widget,lineutils,clipboard,dialog,dialogui,elementspath", "filebrowserUploadUrl": "http://127.0.0.1:8000/api/image/upload/", "filebrowserBrowseUrl": "http://127.0.0.1:8000/ckeditor/browse/", "language": "en-us"}',
      schema: {
        fields: [
          {
            name: 'title',
            placeholder: 'Title',
            value: '',
            required: true,
            label: 'title'
          },
          {
            name: 'subheading',
            placeholder: 'Subheading',
            value: '',
            label: 'Subheading',
            required: true
          }
        ]
      },
      buttonSchema: {
        name: 'Update',
        className: 'btn btn-warning',
        type: 'submit'
      },
      slots: {
        slotNames: [
          {
            name: 'editor'
          },
          {
            name: 'image'
          }
        ]
      }
    }
  },
  head () {
    return {
      title: 'Update Article',
      script: [
        { src: 'http://127.0.0.1:8000/static/ckeditor/ckeditor-init.js' },
        { src: 'http://127.0.0.1:8000/static/ckeditor/ckeditor/ckeditor.js' }
      ]
    }
  },
  created () {
    this.fetchArticleData()
  },
  methods: {
    async fetchArticleData () {
      try {
        await this.$axios
          .get(`api/article/${this.$route.params.slug}/update/`)
          .then((resp) => {
            this.title = resp.data.title
            this.schema.fields[0].value = this.title
            this.subheading = resp.data.subheading
            this.schema.fields[1].value = this.subheading
            setTimeout(() => {
              if (process.client) {
                window.CKEDITOR.instances.id_text.setData(resp.data.text)
              }
            }, 3000)
          })
      } catch (error) {
        this.errors = error.response.data
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
    },
    async articleUpdate () {
      const form = new FormData()
      form.append('title', this.title)
      form.append('subheading', this.subheading)
      form.append('text', window.CKEDITOR.instances.id_text.getData())
      form.append(
        'image',
        this.$refs.file.files[0] ? this.$refs.file.files[0] : ''
      )
      try {
        await this.$axios
          .put(`api/article/${this.$route.params.slug}/update/`, form, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
          // Slugify the title in case title changed
          .then(() => {
            const slug = this.title
              .toLowerCase()
              .replace(/ /g, '-')
              .replace(/[^\w-]+/g, '')
            this.$router.push({ name: 'article-slug', params: { slug } })
          })
      } catch (error) {
        this.errors = error.response.data
      }
    }
  }
}
</script>
