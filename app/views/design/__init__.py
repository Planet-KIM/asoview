
"""/design – ASOdesign 작업 요청."""

from flask import Blueprint, jsonify, request, url_for
from tasks.asodesign import run_asodesign  # noqa: WPS433 – cross‑package import

bp = Blueprint("design", __name__)


@bp.route("/design", methods=["POST"])
def submit_design():
    payload = request.get_json(force=True) or {}

    task = run_asodesign.delay(
        payload.get("transid", "NM_002415"),
        payload.get("query_assembly", ["mm39", "mm10"]),
        payload.get("ref_assembly", "hg38"),
        payload.get("tile_length", 18),
        payload.get("chunk_division", 5),
        payload.get("max_workers", 1),
        payload.get("wobble", 0),
        payload.get("gapmer_filtered", True),
    )

    return (
        jsonify(
            {
                "task_id": task.id,
                "status_url": url_for("status.task_status", task_id=task.id, _external=True),
            }
        ),
        202,
    )