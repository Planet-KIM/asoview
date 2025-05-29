from flask import Blueprint, jsonify
from tasks.asodesign import run_asodesign_process

bp = Blueprint("status", __name__)


@bp.route("/status/<task_id>")
def task_status(task_id):  # noqa: D401
    task = run_asodesign_process.AsyncResult(task_id)

    if task.state == "PENDING":
        response = {"state": task.state}
    elif task.state == "SUCCESS":
        response = {"state": task.state, "result": task.result}
    elif task.state == "FAILURE":
        response = {"state": task.state, "error": str(task.info)}
    else:  # STARTED, RETRY 등
        response = {"state": task.state}

    return jsonify(response)