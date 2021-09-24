web: gunicorn hackernews.wsgi --log-file -
worker: celery -A hackernews worker -l info -B