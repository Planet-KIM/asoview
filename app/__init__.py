# app/__init__.py
import os
from flask import Flask
from celery import Celery

BROKER_URL  = os.getenv("CELERY_BROKER_URL",  "redis://localhost:6379/0")
BACKEND_URL = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery_app = Celery(__name__, broker=BROKER_URL, backend=BACKEND_URL)
celery_app.conf.update(
    worker_pool="solo",            # 프로세스 1개 당 1개 작업 처리 후 재시작
    worker_concurrency=1,
    worker_max_tasks_per_child=1,  # == 작업 1개 처리 뒤 재시작
    result_serializer="json",
    accept_content=["json"],
    task_serializer="json",
)

def _make_celery(app):
    class ContextTask(celery_app.Task):
        def __call__(self, *a, **kw):
            with app.app_context():
                return self.run(*a, **kw)
    celery_app.Task = ContextTask
    return celery_app

def create_app():
    app = Flask(__name__)
    from .views.design import bp as design_bp
    from .views.status import bp as status_bp
    app.register_blueprint(design_bp)
    app.register_blueprint(status_bp)
    _make_celery(app)
    return app