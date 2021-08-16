# django-drf-nuxtjs-blog
A complete blog integrated with Django rest-framework (DRF) and Nuxt js

The project is not ready for production. The purpose of this is to show the combination of these two powerful frameworks.

**About project**
- All authentication system (login, logout, verification email, resend email etc..)
- Users can create-update-delete article, leave or delete their comments
- Users can like/dislike articles and even comments

The template is free and you can get it from [here](https://startbootstrap.com/theme/clean-blog)

**Installation**
```
cd backend
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver 
```
Also on frontend,
```bash
# install dependencies
$ npm install

# serve with hot reload at localhost:3000
$ npm run dev

# build for production and launch server
$ npm run build
$ npm run start

# generate static project
$ npm run generate
```

Enjoy!!!

