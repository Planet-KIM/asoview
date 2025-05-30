# app/celery_worker.py
from app import create_app, celery_app, make_celery

flask_app = create_app()
make_celery(flask_app)