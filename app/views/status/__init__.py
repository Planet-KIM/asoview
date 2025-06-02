from flask import Blueprint, jsonify
from tasks.asodesign import run_asodesign_process

from app.models import TaskRun
from app.utils import compress_folder
import json

bp = Blueprint("status", __name__, url_prefix='/status')


@bp.route("/asodesign/<task_id>")
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


@bp.route('/tasks/data')
def tasks_data():
    """
    JSON으로 TaskRun 목록을 내려주는 API.
    args_json을 파싱하여 parsed_args처럼 필요한 필드를 꺼냅니다.
    모델에 있는 다른 컬럼(user_name, result_json 등)도 함께 반환할 수 있습니다.
    """
    # TaskRun을 최신 id 순서로 조회
    runs = TaskRun.query.order_by(TaskRun.id.desc()).all()
    data = []

    for run in runs:
        # 1) args_json (문자열) → 딕셔너리로 파싱
        try:
            parsed = json.loads(run.args_json) if run.args_json else {}
        except Exception:
            parsed = {}

        # 2) parsed에서 필요한 필드 꺼내기
        transid = parsed.get('transid', '')
        query_assembly = parsed.get('query_assembly', [])
        if not isinstance(query_assembly, list):
            query_assembly = []

        ref_assembly = parsed.get('ref_assembly', '')
        k_min = parsed.get('k_min', '')
        k_max = parsed.get('k_max', '')
        wobble = parsed.get('wobble', '')
        gapmer_filtered = parsed.get('gapmer_filtered', False)

        # 3) 날짜/시간 문자열
        started_str = run.started_at.strftime("%Y-%m-%d %H:%M:%S") if run.started_at else ''
        finished_str = run.finished_at.strftime("%Y-%m-%d %H:%M:%S") if run.finished_at else ''

        # 4) elapsed_sec 문자열
        elapsed_str = f"{run.elapsed_sec:.3f}" if (run.elapsed_sec is not None) else ''

        # 5) result_json 그대로 내려주고 싶다면 (optional)
        #    예: run.result_json 를 그대로 내려주면, 프론트엔드에서 필요할 때 파싱해서 볼 수 있음.
        #    여기서는 필드명만 같이 넘깁니다.
        result_raw = run.result_json or ''
        run.user_name = "default123@***" if run.user_name == None else run.user_name
        run.asonedesign_link = "Not yet." if run.asodesign_link == None else run.asodesign_link
        data.append({
            'id': run.id,
            'task_id': run.task_id,
            'user_name': run.user_name,
            'status': run.status,
            'transid': transid,
            'query_assembly': ",".join(query_assembly),
            'ref_assembly': ref_assembly,
            'k_min': k_min,
            'k_max': k_max,
            'wobble': wobble,
            'gapmer_filtered': gapmer_filtered,
            'asodesign_link': run.asodesign_link,
            'started_at': started_str,
            'finished_at': finished_str,
            'elapsed_sec': elapsed_str,
            'result_json': result_raw,
        })

    return jsonify(data)