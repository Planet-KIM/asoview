import os
from flask import Flask
from celery import Celery

celery = Celery(__name__)


def _make_celery(app):
    """Flask 컨텍스트에서 Celery 설정."""
    celery.conf.broker_url = app.config["CELERY_BROKER_URL"]
    celery.conf.result_backend = app.config["CELERY_RESULT_BACKEND"]

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):  # noqa: D401
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app():
    app = Flask(__name__)

    # 환경 변수로 오버라이드 가능
    app.config.update(
        CELERY_BROKER_URL=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
        CELERY_RESULT_BACKEND=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
        result_serializer="json",
        accept_content=["json"],
        task_serializer="json",
    )

    # 뷰 블루프린트 등록
    from .views.design import bp as design_bp  # noqa: WPS433 – local import
    from .views.status import bp as status_bp  # noqa: WPS433

    app.register_blueprint(design_bp)
    app.register_blueprint(status_bp)

    # Celery 앱과 바인딩
    _make_celery(app)
    return app