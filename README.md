# Django movies backend

in order to deploy this app you need to:
- create ```.env``` file and set all of the required .env variables in compliance with ```.env.example``` file
- create virtual environment with ```python3 -m venv venv```
- source newly created venv ```source venv/bin/activate```
- install dependencies with ```python3 -m pip install -r requirements.txt```
- apply migrations using ```python3 manage.py migrate```
- run servier with ```python3 manage.py runserver```
