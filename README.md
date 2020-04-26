# My Blog
Sample blog web application using Python Django + Postgres.

## How to setup?
### Setup Database:
- Run these below commands in PSQL Shell:
    ```postgresql
    CREATE DATABASE blogdb;
  
    CREATE USER blogdbuser WITH PASSWORD 'YOUR_PASSWORD';
  
    ALTER ROLE blogdbuser SET client_encoding TO 'utf8';
    ALTER ROLE blogdbuser SET default_transaction_isolation TO 'read committed';
    ALTER ROLE blogdbuser SET timezone TO 'UTC';
  
    GRANT ALL PRIVILEGES ON DATABASE blogdb TO blogdbuser;
    ```

Remember the values you've entered above. It'll be helpful in upcoming steps.
    
### Setup Project:

- Go to [`settings.py`](MyBlogApp/settings.py) and change the values of these fields:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_PASSWORD',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

- Install Requirements:

```shell script
pip install -r requirements.txt
```

- Setup Initial Database structure:
```shell script
python manage.py makemigrations
python manage.py migrate
```

- Create superuser
```shell script
python manage.py createsuperuser
```

- Run App
```shell script
python manage.py runserver
```

Now after succesfully executing above commands, visit below URL's to test this app.

Function      | Description          | URL
------------- | -------------------  | -------------
Admin         | Django Admin Panel   | [`localhost:8000/admin`](http://localhost:8000/admin)
Blog App      | Blog App UI          | [`localhost:8000/blog`](http://localhost:8000/blog)
API           | REST API             | [`localhost:8000/api`](http://localhost:8000/api)

## Tasks
- [x] User Authentication
- [x] Add/Edit/Delete Posts
- [x] Add/Edit/Delete Categories (Using Django Admin)
- [x] Listing Posts
- [x] Filter by Category
- [x] Filter by Tags
- [x] Tests
- [x] REST API for posts
