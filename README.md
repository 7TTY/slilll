# Simple Flask CRUD Web Application
This is a very simple Flask Application where user can log in and create posts.

## Deploying Locally
Lets walk through setting up your development environment and deploying this application on your local machine

1. Install Python, pip, and virtualenv
  - [Python](https://www.python.org/)
  - [pip](https://pip.pypa.io/en/stable/installing/)
  - [Virtualenv](https://virtualenv.pypa.io/en/latest/installation/)

4. Install packages
```
pip install -r flask_app/requirements.txt
```
5. Create Flask environment variables
```
export FLASK_APP=flask_app/__init__.py
export FLASK_ENV=development
```
6. Run it
```
flask run
```

