# CENs

Repository for the backend that deals with Contact Event Numbers (CENs)

## Setting up dev environment

Install all python modules by running

```
pip install -r requirements.txt
```

For the dev environment, we can simply use SQLite. Make sure you have it installed on your machine and then create the database by running

```
flask db upgrade
```

To run the app, first make sure the `FLASK_APP` environment variable is set:

```
export FLASK_APP="app:create_app('dev')"
```

Then run the app with

```
flask run
```

## Testing

To run tests, call

```
python -m pytest
```
