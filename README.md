generic-django-project
======================


Generic project directory structure for new django applications.

For more info, read my blog post:

https://medium.com/cs-math/f29f6080c131


#### Installation on Heroku

If you want to use Heroku to host your Django application, checkout this project

https://github.com/josephmisiti/generic-django-project-heroku

Just follow directions and you should have a django app running on Heroku in a few steps!

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

I like to use postgres, so I suggest installing [PostGreApp](http://postgresapp.com/). Once that is installed,
execute the following commands

```
$ createdb <DBNAME>
```

Then sync and execute migrations

```
$ python manage.py syncdb
$ python manage.py migrate
```

Done! If you are not using OSX, you're on your own. It's pretty easy to install Postgres on UBUNTU (see fabfile.py), but I have no experience on Windows.


If you have any questions or what to help out, send a pull request or reach out at [@josephmisiti](http://www.twitter.com/josephmisiti)
