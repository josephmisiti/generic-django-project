generic-django-project
======================

Generic project directory structure for new django applications.

For more info, read my blog post:

https://medium.com/cs-math/f29f6080c131


#### Installation

First, get cookiecutter

```
$ pip install cookiecutter
```

Then execute the following command:

```
$ cookiecutter https://github.com/josephmisiti/generic-django-project.git
```

#### Setting Up The Database

I like to use postgres, so I suggest install [PostGreApp](http://postgresapp.com/). One that is installed
execute the following commands

```
$ createdb <DBNAME>
```

Then sync and execute migrations

```
$ python manage.py syncdb
$ python manage.py migrate
```

Done !
