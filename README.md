# PromptHub Backend

* python: 3.9
* django: 4.1.7

### usage

* migrate database

```shell
$ python manage.py makemigrations core
$ python manage.py migrate
```

* run server

```shell
$ python manage.py runserver
```

* ruff check and fix

```shell
$ ruff check . --fix
```

* unittest 

```shell
$ python manage.py test tests
```

* coverage

```shell
$ coverage python manage.py test tests
$ coverage html
```