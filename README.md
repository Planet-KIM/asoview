# asoview
## Make the website using flask and asopipe modules
# 프로젝트 구조
# ─────────────────────────────────────────
# app/              → Flask 애플리케이션 + Blueprints
#     __init__.py   → 앱 팩토리, Celery 바인딩
#     views/
#         __init__.py
#         /design/__init__.py → /design 엔드포인트
#         /status/__init__.py → /status/<id> 엔드포인트
# tasks/
#     __init__.py
#     asodesign.py  → Celery 장기 실행 Task
# manage.py         → 개발서버 진입점 (gunicorn 사용 시 WSGI 대상)
# requirements.txt  → 최소 의존 목록
#
# Python 3.8 호환 & typing 미사용 버전