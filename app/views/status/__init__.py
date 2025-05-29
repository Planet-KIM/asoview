from flask import Blueprint, jsonify
from tasks.asodesign import run_asodesign_process
from app.utils import compress_folder

bp = Blueprint("status", __name__)


@bp.route("/status/asodesign/<task_id>")
def asodesign_task_status(task_id):  # noqa: D401
    task = run_asodesign_process.AsyncResult(task_id)

    if task.state == "PENDING":
        response = {"state": task.state, 
                    "task_id": task.id}
    elif task.state == "SUCCESS":
        # 작업 완료 후 폴더 압축    
        # 문제가 하나있다면 해당 페이지를 방문해야지 파일을 압축한다는 것이다 만약 바로 파일을 다운로드하고 싶다면 파일이 업는 경우가 생길 수 있다.
        # 따라서 이 부분은 나중에 개선이 필요하다.
        task_id = task.id
        compress_folder(task_id)
        response = {"state": task.state,
                    "task_id": task.id,
                    "result": task.result}
    elif task.state == "FAILURE":
        response = {"state": task.state, "task_id": task.id, "error": str(task.info)}
    else:  # STARTED, RETRY 등
        response = {"state": task.state}

    return jsonify(response)