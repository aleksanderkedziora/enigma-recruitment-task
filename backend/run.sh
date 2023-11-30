#!/bin/sh

set -e

# Specify the name of your virtual environment
venv_name="devenv"

pip install virtualenv  # Install virtualenv if not already installed
virtualenv "$venv_name"

ls -l "$venv_name"

# Activate the virtual environment
source "$venv_name/bin/activate"

# Install dependencies or perform other setup steps
pip install -r requirements.txt

nohup redis-server &

nohup celery -A config  worker -l info &
nohup celery -A config  beat -l INFO &

python manage.py migrate
python manage.py runserver 8000

