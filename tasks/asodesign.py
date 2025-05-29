"""Celery Task – ASOdesign 실행."""

import multiprocessing as mp
import time
import sys
sys.path.append("/Users/dowonkim/Dropbox/data/celery_asodesign/mypkg/")
from asopipe.main import run_ASOdesign#ASOdesign
from app import celery


@celery.task
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
    max_workers = 1
    print(
        f"transid: {transid}, query_assemblies: {query_assemblies}, ref_assembly: {ref_assembly}, "
        f"k_min: {k_min}, k_max: {k_max}, chunk_division: {chunk_division}, max_workers: {max_workers}, wobble: {wobble}, gapmer_filtered: {gapmer_filtered}",
        type(transid), type(query_assemblies), type(ref_assembly), type(k_min), type(k_max), type(chunk_division), type(max_workers), type(wobble), type(gapmer_filtered)
    )
    result  = run_ASOdesign(transid=transid,
                    query_assembly=query_assemblies,
                    ref_assembly=ref_assembly,
                    k_min=k_min, k_max=k_max,
                    chunk_division=chunk_division, max_workers=max_workers, wobble=wobble, to_df=False, gapmer_filtered=gapmer_filtered,
                    to_csv=True, output_path=f"/Users/dowonkim/Dropbox/data/celery_asodesign/asoview/design_folder/")
    print(result)

    return {
        "elapsed_sec": round(time.perf_counter() - start, 3),
        "records": result,
    }
    
    