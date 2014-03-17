web: newrelic-admin run-program gunicorn --chdir src project.wsgi:application --bind 0.0.0.0:$PORT --workers $WEB_CONCURRENCY --config gunicorn.conf.py
worker: celery worker --app project --workdir src
