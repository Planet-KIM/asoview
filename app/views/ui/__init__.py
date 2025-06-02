# app/views/ui/__init__.py
import json
import time
from hashlib import sha256

from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import TaskRun
from tasks.asodesign import run_asodesign_process  # Celery 태스크

ui_bp = Blueprint("ui", __name__, template_folder="templates")


def _as_int(v, default):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


@ui_bp.route("/tasks", methods=["GET", "POST"])
def tasks():
    if request.method == "POST":
        # ── 입력값 파싱 ────────────────────────────────────────────
        user_name = "default123@***"
        transid = request.form.get("transid", "").strip()
        query_assembly = request.form.get("query_assembly", "").strip()
        ref_assembly = request.form.get("ref_assembly", "").strip()

        if query_assembly:
            q_list = [s.strip() for s in query_assembly.split(",") if s.strip()]
        else:
            q_list = []

        k_min = _as_int(request.form.get("k_min"), 18)
        k_max = _as_int(request.form.get("k_max"), 18)
        wobble = _as_int(request.form.get("wobble"), 0)
        gapmer_filtered = request.form.get("gapmer_filtered") == "on"

        if not transid:
            flash("transid는 비어 있을 수 없습니다.", "warning")
            return redirect(url_for("ui.tasks"))

        args_dict = {
            "transid": transid,
            "query_assembly": q_list,
            "ref_assembly": ref_assembly,
            "k_min": k_min,
            "k_max": k_max,
            "wobble": wobble,
            "gapmer_filtered": gapmer_filtered,
        }
        args_json = json.dumps(args_dict, sort_keys=True, separators=(",", ":"))
        args_hash = sha256(args_json.encode("utf-8")).hexdigest()
        

        cached = None
        if args_hash:
            cached = TaskRun.query.filter_by(args_hash=args_hash, status="SUCCESS").first()
        if cached:
            # 동일한 입력값으로 이미 존재하는 작업이 있다면 flash로 알려주고 해당 작업을 테이블에서 찾을 수 있게 함
            flash(f"동일한 파라미터로 이미 생성된 작업이 있습니다. Task ID: {cached.task_id}", "info")
            #flash("동일 파라미터로 이미 완료된 작업이 있습니다.", "info")
            return redirect(url_for("ui.tasks"))

        task = run_asodesign_process.delay(
            transid,
            q_list,
            ref_assembly,
            k_min,
            k_max,
            wobble,
            gapmer_filtered,
        )

        new_run = TaskRun(
            task_id=task.id,
            user_name=user_name,
            status="PENDING",
            args_json=args_json,
            args_hash=args_hash,
            started_at=time.strftime("%Y/%m/%d/%H:%M:%S", time.localtime(time.time())),
            asodesign_link="Not yet."
        )
        try:
            db.session.add(new_run)
            db.session.commit()
            flash(f"새 태스크 {task.id} 이(가) 생성되었습니다.", "success")
        except IntegrityError:
            db.session.rollback()
            flash("해시 중복 또는 DB 오류가 발생했습니다. 기존 캐시를 사용합니다.", "warning")

        return redirect(url_for("ui.tasks"))

    # ── GET: TaskRun 레코드 조회 + JSON 파싱 ─────────────────────────────
    runs = TaskRun.query.order_by(TaskRun.id.desc()).all()

    # 각 run 객체에 parsed_args 속성을 붙여둡니다.
    for run in runs:
        try:
            run.parsed_args = json.loads(run.args_json)
        except Exception:
            run.parsed_args = {}

    return render_template("tasks.html", runs=runs)