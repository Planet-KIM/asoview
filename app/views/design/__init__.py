
"""/design – ASOdesign 작업 요청."""

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

    transid = payload.get("transid", "NM_002415")

    query_assembly = payload.get("query_assembly", ["mm39", "mm10"])
    # GET ?query_assembly=mm39,mm10  → 리스트 변환
    if isinstance(query_assembly, str):
        query_assembly = [s.strip() for s in query_assembly.split(",") if s.strip()]

    ref_assembly = payload.get("ref_assembly", "hg38")
    k_min = _as_int(payload.get("k_min"), 18)
    k_max = _as_int(payload.get("k_max"), 18)
    wobble = _as_int(payload.get("wobble"), 0)
    gapmer_filtered = str(payload.get("gapmer_filtered", "true")).lower() == "true"

    # ── Celery 비동기 작업 발행 ─────────────────────────────
    task = run_asodesign_process.delay(
        transid=transid,
        query_assemblies=query_assembly,
        ref_assembly=ref_assembly,
        k_min=k_min,
        k_max=k_max,
        wobble=wobble,
        gapmer_filtered=gapmer_filtered,
    )

    # 202 Accepted + status URL 반환
    return (
        jsonify(
            {
                "task_id": task.id,
                "status_url": url_for("status.asodesign_task_status", task_id=task.id, _external=True),
            }
        ),
        202,
    )