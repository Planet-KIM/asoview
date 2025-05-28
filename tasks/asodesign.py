"""Celery Task – ASOdesign 실행."""

import multiprocessing as mp
import time
from asopipe.main import ASOdesign
from app import celery


@celery.task(bind=True)
def run_asodesign(
    self,
    transid,
    query_assemblies,
    ref_assembly,
    tile_length=18,
    chunk_division=5,
    max_workers=1,
    wobble=0,
    gapmer_filtered=True,
):
    mp.set_start_method("spawn", force=True)
    start = time.perf_counter()

    aso = ASOdesign(
        transid=transid,
        query_assembly=query_assemblies,
        ref_assembly=ref_assembly,
        tile_length=tile_length,
    )

    df = aso.process_main(
        chunk_division=chunk_division,
        max_workers=max_workers,
        wobble=wobble,
        to_df=True,
        gapmer_filtered=gapmer_filtered,
    )

    return {
        "elapsed_sec": round(time.perf_counter() - start, 3),
        "n_candidates": len(df),
        "records": df.to_dict(orient="records"),
    }