# app/__init__.py
import os
from flask import Flask
from celery import Celery

BROKER_URL  = os.getenv("CELERY_BROKER_URL",  "redis://localhost:6379/0")
BACKEND_URL = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery = Celery(__name__, broker=BROKER_URL, backend=BACKEND_URL)
celery.conf.update(
    worker_pool="solo",            # 프로세스 1개
    worker_concurrency=1,
    worker_max_tasks_per_child=1,  # == 작업 1개 처리 뒤 재시작
    result_serializer="json",
    accept_content=["json"],
    task_serializer="json",
)

def _make_celery(app):
    class ContextTask(celery.Task):
        def __call__(self, *a, **kw):
            with app.app_context():
                return self.run(*a, **kw)
    celery.Task = ContextTask
    return celery

def create_app():
    app = Flask(__name__)
    from .views.design import bp as design_bp
    from .views.status import bp as status_bp
    app.register_blueprint(design_bp)
    app.register_blueprint(status_bp)
    _make_celery(app)
    return app