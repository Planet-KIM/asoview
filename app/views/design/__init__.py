
"""/design – ASOdesign 작업 요청."""
import json
import time
from app import db
from app.models import TaskRun
from hashlib import sha256
from flask import Blueprint, jsonify, request, url_for
from tasks.asodesign import run_asodesign_process  # noqa: WPS433 – cross‑package import

bp = Blueprint("design", __name__)


def _as_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
    

@bp.route("/design", methods=["POST", "GET"])
def submit_design():
    # ── 입력 파싱 ───────────────────────────────────────────
    if request.method == "POST":
        payload = request.get_json(force=True) or {}
    else:  # GET
        payload = request.args.to_dict(flat=True)
    # after user name of session
    user_name = "default123@***"
    query_assembly = payload.get("query_assembly", ["mm39", "mm10"])
    # GET ?query_assembly=mm39,mm10  → 리스트 변환
    if isinstance(query_assembly, str):
        query_assembly = [s.strip() for s in query_assembly.split(",") if s.strip()]

    args = {
        "transid": payload.get("transid", "NM_002415"),
        "query_assembly": query_assembly,
        "ref_assembly": payload.get("ref_assembly", "hg38"),
        "k_min": _as_int(payload.get("k_min"), 18),
        "k_max": _as_int(payload.get("k_max"), 18),
        "wobble": _as_int(payload.get("wobble"), 0),
        "gapmer_filtered": str(payload.get("gapmer_filtered", "true")).lower() == "true",
    }
    
    args_json = json.dumps(args, sort_keys=True, separators=(",", ":"))
    args_hash = sha256(args_json.encode()).hexdigest()
    # -------- cache hit? ---------
    hit = TaskRun.query.filter_by(args_hash=args_hash, status="SUCCESS").first()
    #print(hit.args_json, args_json)
    #print(type(json.loads(hit.result_json)))
    if hit:
        return jsonify({    
            "cached": True,
            "user_name": user_name,
            "task_id": hit.task_id,
            "result": json.loads(hit.result_json),
        }), 200
    
    # ── Celery 비동기 작업 발행 ─────────────────────────────
    task = run_asodesign_process.delay(*args.values())

    # pre‑insert PENDING row (ignore if duplicate hash)
    try:
        db.session.add(TaskRun(
            task_id=task.id,
            user_name=user_name,
            status="PENDING",
            args_json=args_json,
            args_hash=args_hash,
            started_at=time.strftime("%Y/%m/%d/%H:%M:%S", time.localtime(time.time())),
        ))
        db.session.commit()
    except Exception:
        db.session.rollback()

    return jsonify({
        "cached": False,
        "task_id": task.id,
        "status_url": url_for("status.asodesign_task_status", task_id=task.id, _external=True),
    }), 202