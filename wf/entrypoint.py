from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, input: LatchFile, input_basedir: typing.Optional[LatchDir], outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], max_length: typing.Optional[int], min_length: typing.Optional[int], dedup: typing.Optional[bool], remove_polyg: typing.Optional[bool], demux_min_length: typing.Optional[int], markers_ignore: typing.Optional[str], collapse_use_counts: typing.Optional[bool], min_size: typing.Optional[int], max_size: typing.Optional[int], skip_analysis: typing.Optional[bool], use_full_bipartite: typing.Optional[bool], skip_layout: typing.Optional[bool], skip_report: typing.Optional[bool], pixelator_container: typing.Optional[str], trim_front: typing.Optional[int], trim_tail: typing.Optional[int], max_n_bases: typing.Optional[int], avg_qual: typing.Optional[int], adapterqc_mismatches: typing.Optional[float], demux_mismatches: typing.Optional[float], algorithm: typing.Optional[str], collapse_mismatches: typing.Optional[int], collapse_min_count: typing.Optional[int], multiplet_recovery: typing.Optional[bool], dynamic_filter: typing.Optional[str], aggregate_calling: typing.Optional[bool], compute_polarization: typing.Optional[bool], compute_colocalization: typing.Optional[bool], polarization_transformation: typing.Optional[str], polarization_n_permutations: typing.Optional[int], polarization_min_marker_count: typing.Optional[int], colocalization_transformation: typing.Optional[str], colocalization_neighbourhood_size: typing.Optional[int], colocalization_n_permutations: typing.Optional[int], colocalization_min_region_count: typing.Optional[int], no_node_marker_counts: typing.Optional[bool], layout_algorithm: typing.Optional[str]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('input', input),
                *get_flag('input_basedir', input_basedir),
                *get_flag('outdir', outdir),
                *get_flag('email', email),
                *get_flag('trim_front', trim_front),
                *get_flag('trim_tail', trim_tail),
                *get_flag('max_length', max_length),
                *get_flag('min_length', min_length),
                *get_flag('max_n_bases', max_n_bases),
                *get_flag('avg_qual', avg_qual),
                *get_flag('dedup', dedup),
                *get_flag('remove_polyg', remove_polyg),
                *get_flag('adapterqc_mismatches', adapterqc_mismatches),
                *get_flag('demux_mismatches', demux_mismatches),
                *get_flag('demux_min_length', demux_min_length),
                *get_flag('markers_ignore', markers_ignore),
                *get_flag('algorithm', algorithm),
                *get_flag('collapse_mismatches', collapse_mismatches),
                *get_flag('collapse_min_count', collapse_min_count),
                *get_flag('collapse_use_counts', collapse_use_counts),
                *get_flag('multiplet_recovery', multiplet_recovery),
                *get_flag('min_size', min_size),
                *get_flag('max_size', max_size),
                *get_flag('dynamic_filter', dynamic_filter),
                *get_flag('aggregate_calling', aggregate_calling),
                *get_flag('skip_analysis', skip_analysis),
                *get_flag('compute_polarization', compute_polarization),
                *get_flag('compute_colocalization', compute_colocalization),
                *get_flag('use_full_bipartite', use_full_bipartite),
                *get_flag('polarization_transformation', polarization_transformation),
                *get_flag('polarization_n_permutations', polarization_n_permutations),
                *get_flag('polarization_min_marker_count', polarization_min_marker_count),
                *get_flag('colocalization_transformation', colocalization_transformation),
                *get_flag('colocalization_neighbourhood_size', colocalization_neighbourhood_size),
                *get_flag('colocalization_n_permutations', colocalization_n_permutations),
                *get_flag('colocalization_min_region_count', colocalization_min_region_count),
                *get_flag('skip_layout', skip_layout),
                *get_flag('no_node_marker_counts', no_node_marker_counts),
                *get_flag('layout_algorithm', layout_algorithm),
                *get_flag('skip_report', skip_report),
                *get_flag('pixelator_container', pixelator_container)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_pixelator", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_pixelator(input: LatchFile, input_basedir: typing.Optional[LatchDir], outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], max_length: typing.Optional[int], min_length: typing.Optional[int], dedup: typing.Optional[bool], remove_polyg: typing.Optional[bool], demux_min_length: typing.Optional[int], markers_ignore: typing.Optional[str], collapse_use_counts: typing.Optional[bool], min_size: typing.Optional[int], max_size: typing.Optional[int], skip_analysis: typing.Optional[bool], use_full_bipartite: typing.Optional[bool], skip_layout: typing.Optional[bool], skip_report: typing.Optional[bool], pixelator_container: typing.Optional[str], trim_front: typing.Optional[int] = 0, trim_tail: typing.Optional[int] = 0, max_n_bases: typing.Optional[int] = 0, avg_qual: typing.Optional[int] = 20, adapterqc_mismatches: typing.Optional[float] = 0.1, demux_mismatches: typing.Optional[float] = 0.1, algorithm: typing.Optional[str] = 'adjacency', collapse_mismatches: typing.Optional[int] = 2, collapse_min_count: typing.Optional[int] = 2, multiplet_recovery: typing.Optional[bool] = True, dynamic_filter: typing.Optional[str] = 'min', aggregate_calling: typing.Optional[bool] = True, compute_polarization: typing.Optional[bool] = True, compute_colocalization: typing.Optional[bool] = True, polarization_transformation: typing.Optional[str] = 'log1p', polarization_n_permutations: typing.Optional[int] = 50, polarization_min_marker_count: typing.Optional[int] = 5, colocalization_transformation: typing.Optional[str] = 'log1p', colocalization_neighbourhood_size: typing.Optional[int] = 1, colocalization_n_permutations: typing.Optional[int] = 50, colocalization_min_region_count: typing.Optional[int] = 5, no_node_marker_counts: typing.Optional[bool] = False, layout_algorithm: typing.Optional[str] = 'pmds_3d') -> None:
    """
    nf-core/pixelator

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, input=input, input_basedir=input_basedir, outdir=outdir, email=email, trim_front=trim_front, trim_tail=trim_tail, max_length=max_length, min_length=min_length, max_n_bases=max_n_bases, avg_qual=avg_qual, dedup=dedup, remove_polyg=remove_polyg, adapterqc_mismatches=adapterqc_mismatches, demux_mismatches=demux_mismatches, demux_min_length=demux_min_length, markers_ignore=markers_ignore, algorithm=algorithm, collapse_mismatches=collapse_mismatches, collapse_min_count=collapse_min_count, collapse_use_counts=collapse_use_counts, multiplet_recovery=multiplet_recovery, min_size=min_size, max_size=max_size, dynamic_filter=dynamic_filter, aggregate_calling=aggregate_calling, skip_analysis=skip_analysis, compute_polarization=compute_polarization, compute_colocalization=compute_colocalization, use_full_bipartite=use_full_bipartite, polarization_transformation=polarization_transformation, polarization_n_permutations=polarization_n_permutations, polarization_min_marker_count=polarization_min_marker_count, colocalization_transformation=colocalization_transformation, colocalization_neighbourhood_size=colocalization_neighbourhood_size, colocalization_n_permutations=colocalization_n_permutations, colocalization_min_region_count=colocalization_min_region_count, skip_layout=skip_layout, no_node_marker_counts=no_node_marker_counts, layout_algorithm=layout_algorithm, skip_report=skip_report, pixelator_container=pixelator_container)

