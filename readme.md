# IMDB Clone API
## Date of project creation: May 2022
## 1. Project Description
* Small showcase project in DjangoRestFramework
* Containes Platform database model which can be represented with Netflix, AmazonPrime, HBO etc.
* Contains Watchlist database model which can be represented with various Movies, Documentaries, TV shows etc.
* Contains Review database model provided for Users for adding reviews and rating to specific Movie
* User registration and login is also implemented
* Only admin who is superuser can create or modify Platforms and Watchlists and admin can also modify Reviews
* Filtering is added for specific routes

## 2. ⚙️ Dev stack
**`Python`**  (v3.8.10)<br />
**`PIP`**  (v21.3.1)<br />
**`Django`**  (v4.0.4)<br />
**`DjangoRestFramework`**  (v3.13.1)<br />

## 3. Project Setup ##
**install virtual environment**\
`sudo pip install virtualenv`

**create virtual environment**\
`virtualenv venv`
or
`virtualenv --python=/usr/bin/python3 venv`

**activate virtual environment**\
`source venv/bin/activate`

**install requirements**\
`pip install -r requirements.txt`

**django secret key**
* generate django secret key at: https://djecrety.ir/
* paste it in settings.SECRET_KEY

**database info**
* project is configured for SQLite but if you want other databases, configure your settings file and install corresponding database engine

**migrate database**\
`python manage.py migrate`

**admin registration info**\
`python manage.py createsuperuser`

**run django server**\
`python manage.py runserver`

**registration info**
* enter username,email,password,password2 in Postman for obtaining Token
* When you register or log user in, set header Authorization as key and Token{value} as value

## 4. List of available API routes
**Register Account**\
`POST: http://127.0.0.1:8000/account/register/`\
**Login Account**\
`POST: http://127.0.0.1:8000/account/login/`\
**Get Stream List (With Movies that belong to specific list)**\
`GET: http://127.0.0.1:8000/watch/stream/`\
**Create Stream (Only allowed to superuser/admin)**\
`POST: http://127.0.0.1:8000/watch/stream/`\
**Get specific Stream (shows all watchlist that belongs to stream)**\
`GET: http://127.0.0.1:8000/watch/stream/{id}`\
**Update specific Stream (Only allowed to superuser/admin)**\
`PUT: http://127.0.0.1:8000/watch/stream/{id}`\
**Delete specific Stream (Only allowed to superuser/admin)**\
`DELETE: http://127.0.0.1:8000/watch/stream/{id}`\
**Get Watchlist (allowed to everyone)**\
`GET: http://127.0.0.1:8000/watch/list/`\
**Create Watchlist (Only allowed to superuser/admin)**\
`POST: http://127.0.0.1:8000/watch/list/`\
**View specific Watchlist(Movie)**\
`GET: http://127.0.0.1:8000/watch/{id}/`\
**Update specific Watchlist/Movie (Only allowed to superuser/admin)**\
`PUT: http://127.0.0.1:8000/watch/{id}/`\
**Delete specific Watchlist/Movie (Only allowed to superuser/admin)**\
`DELETE: http://127.0.0.1:8000/watch/{id}/`\
**Get all reviews for specific Watchlist/Movie**\
`GET: http://127.0.0.1:8000/watch/{id}/review/`\
**Create review for specific movie (allowed to everyone)**\
`POST: http://127.0.0.1:8000/watch/{id}/review_create/`\
**View specific review for specific movie**\
`GET: http://127.0.0.1:8000/watch/review/{id}/`\
**Update specific review for specific movie (review author or admin can modify)**\
`PUT: http://127.0.0.1:8000/watch/review/{id}/`\
**Delete specific review for specific movie (review author or admin can delete)**\
`DELETE: http://127.0.0.1:8000/watch/review/{id}/`\
**View reviews from specific username**\
`GET: http://127.0.0.1:8000/watch/review/?username={username}`\
**Filtering reviews for specific Movie**\
`GET: http://127.0.0.1:8000/watch/{id}/review?review_user__username={review_user}`\
`GET: http://127.0.0.1:8000/watch/{id}/review?active={active}`\
**Filtering Watchlist**\
`GET: http://127.0.0.1:8000/watch/list?platform__name={platform}`\
`GET: http://127.0.0.1:8000/watch/list?title={title}`\