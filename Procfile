web: gunicorn runp-heroku:app
init: export FLASK_APP=run.py && flask db upgrade
upgrade: export FLASK_APP=run.py && flask db upgrade