# What is it

This is a simple backend, written in Django, for storing the random identifiers created by the CovidWatch bluetooth project

# How to run it

* Check out the repo
* Make sure you have a PostgreSQL instance running
  * on localhost
  * database `covid19`
  * username `postgres`
* (optional) make a virtualenv
* install python requirements: `pip install -r requirements.txt`
  * On Mac/Catalina, you may need to comment out django_heroku to get this to run
* set a SECRET_KEY (random 50 character string) and an ENV (dev) in your environment
  * Best to do this with a script, or as part of virtualenv's `activate`

* `./manage.py migrate`
* `./manage.py runserver`

You now have the API running on localhost:8000
