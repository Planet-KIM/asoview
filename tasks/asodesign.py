"""Celery Task – ASOdesign 실행."""

import multiprocessing as mp
import hashlib
import json
import time
import sys
import os
#sys.path.append("../")
from asopipe.main import run_ASOdesign#ASOdesign
from app import celery_app, db
from app.models import TaskRun
from app.utils import compress_folder, make_asodesign_link
from celery import current_task


@celery_app.task
def run_asodesign_process(
    transid="NM_002415",
    query_assemblies=["mm39", "mm10"],
    ref_assembly="hg38",
    k_min=18,
    k_max=20,
    chunk_division=5,
    max_workers=1,
    wobble=0,
    gapmer_filtered=True
    ):
    mp.set_start_method("spawn", force=True)
    start = time.perf_counter()
    chunk_division = 5
    max_workers = 5
    task_id = current_task.request.id

    #
    #start_ts = time.strftime("%Y/%m/%d/%H:%M:%S", time.localtime(time.time()))
    try:
        current_path = os.path.dirname(os.path.realpath(__file__))
        output_path = os.path.join(current_path, f"../design_folder/{task_id}/")
        if not os.path.exists(output_path):
            os.makedirs(output_path, exist_ok=True)
        result  = run_ASOdesign(transid=transid,
                        query_assembly=query_assemblies,
                        #refFlat_path = "/home/commons/Reference/UCSC/hg38/refseq/refFlat_200817.txt",
                        #maf_dir='/home/commons/Reference/UCSC/hg38/maf',
                        #dbsnp_path ="/home/jkportal/data/VCF/dbsnp.bcf",
                        #dbsnp_index_path ="/home/jkportal/data/VCF/dbsnp.bcf.csi",
                        ref_assembly=ref_assembly,
                        k_min=k_min, k_max=k_max,
                        chunk_division=chunk_division, max_workers=max_workers, wobble=wobble, to_df=False, gapmer_filtered=gapmer_filtered,
                        to_csv=True, output_path=output_path)

        elapsed_time = round(time.perf_counter() - start, 3)
        result_obj = {
            "elapsed_sec": round(time.perf_counter() - start, 3),
            "records": result,
            "id": task_id
        }

        tr = TaskRun.query.filter_by(task_id=task_id).first()
        if tr:
        # --------------- DB: 성공 업데이트 ------------------------------
            tr.status       = "SUCCESS"
            #tr.args_json = args_json
            #tr.result_json  = json.dumps(result_obj)
            tr.finished_at  = time.strftime("%Y/%m/%d/%H:%M:%S", time.localtime(time.time()))
            tr.elapsed_sec  = elapsed_time
            #tr.args_hash = args_hash
            iscompress_path = compress_folder(task_id, base_dir=None)
            tr.asodesign_link = make_asodesign_link(task_id, html_name="ASO Design files(gzip)",
                            host="/", api="ftp/design/result/gz/", cache_path='design_folder/')
            
            db.session.commit()
        return result_obj
    except Exception as e:
        tr.status = "FAILURE"
        #tr.result_json = json.dumps({"error": str(e)})
        db.session.commit()
        raise e


