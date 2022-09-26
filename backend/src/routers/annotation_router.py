""" Annotation endpoint routes that handle all things annotation within the application """

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from ..enums import GenomicUnitType

from ..core.annotation import AnnotationService
from ..dependencies import database, annotation_queue
from ..models.analysis import Analysis

router = APIRouter(
    prefix="/annotate",
    tags=["annotation"],
    dependencies=[Depends(database), Depends(annotation_queue)],
)

@router.post("/{name}", status_code=status.HTTP_202_ACCEPTED)
def annotate_analysis(
    name: str,
    background_tasks: BackgroundTasks,
    collections=Depends(database),
    annotation_task_queue=Depends(annotation_queue),
):
    """
    Placeholder to initiate annotations for an analysis. This queueing/running
    annotations for a sample will be moved to the analysis creation endpoint
    when it is created in an upcomming update.
    """
    analysis_json = collections["analysis"].find_by_name(name)
    if analysis_json is None:
        raise HTTPException(status_code=404, detail=f"'{name}' Analysis not found.")

    analysis = Analysis(**analysis_json)
    annotation_service = AnnotationService(collections["annotation_config"])
    annotation_service.queue_annotation_tasks(analysis, annotation_task_queue)
    background_tasks.add_task(AnnotationService.process_tasks, annotation_task_queue, collections['genomic_unit'])

    return {"name": f"{name} annotations queued."}

@router.get("/annotate-beat")
def heartbeat():
    """Returns a heart-beat that orchestration services can use to determine if the application is running"""
    return "thump-thump"

@router.get("/gene/{gene}")
def get_annotations_by_gene(gene, rosalution_db=Depends(database)):
    """Returns annotations data by calling method to find annotations by gene"""

    genomic_unit = {
        'type': GenomicUnitType.GENE,
        'unit': gene,
    }

    queried_genomic_unit = rosalution_db["genomic_unit"].find_genomic_unit(genomic_unit)

    if queried_genomic_unit is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return queried_genomic_unit['annotations']

@router.get("/hgvsVariant/{variant}")
def get_annotations_by_hgvs_variant(variant: str, rosalution_db=Depends(database)):
    """Returns annotations data by calling method to find annotations for variant and relevant transcripts
    by HGVS Variant"""

    genomic_unit = {
        'type': GenomicUnitType.HGVS_VARIANT,
        'unit': variant,
    }

    queried_genomic_unit = rosalution_db["genomic_unit"].find_genomic_unit(genomic_unit)

    if queried_genomic_unit is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return queried_genomic_unit['annotations'] + queried_genomic_unit['transcripts']
