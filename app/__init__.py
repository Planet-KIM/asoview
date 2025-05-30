import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from celery import Celery

db = SQLAlchemy()

MYSQL_URI = os.getenv(
    "MYSQL_URI",
    "mysql+pymysql://root:rla5920!@127.0.0.1:3306/aso_portal?charset=utf8mb4",
)

BROKER_URL  = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
BACKEND_URL = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery_app = Celery(__name__, broker=BROKER_URL, backend=BACKEND_URL)
celery_app.conf.update(
    worker_pool="solo",
    worker_concurrency=1,
    worker_max_tasks_per_child=1,
    result_serializer="json",
    accept_content=["json"],
    task_serializer="json",
)

def make_celery(app):
    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = MYSQL_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # 블루프린트 등록
    from .views.design import bp as design_bp
    from .views.status import bp as status_bp
    app.register_blueprint(design_bp)
    app.register_blueprint(status_bp)

    make_celery(app)  # 컨텍스트 연결
    return app