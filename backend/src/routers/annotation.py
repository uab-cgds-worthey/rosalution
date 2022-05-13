from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status

from ..annotation import AnnotationService
from ..dependencies import database, annotation_queue
from ..core.analysis import Analysis

router = APIRouter(
    prefix="/annotate",
    tags=["annotation"],
    dependencies=[Depends(database), Depends(annotation_queue)]
)

@router.post('/{name}', status_code=status.HTTP_202_ACCEPTED)
def annotate_analysis(
  name: str,
  background_tasks: BackgroundTasks,
  collections=Depends(database),
  annotation_task_queue=Depends(annotation_queue)
):
    """
    Placeholder to initiate annotations for an analysis. This queueing/running
    annotations for a sample will be moved to the analysis creation endpoint
    when it is created in an upcomming update.
    """
    analysis_json = collections['analysis'].find_by_name(name)
    if analysis_json is None:
        raise HTTPException(
            status_code=404, detail=f"'{name}' Analysis not found.")

    analysis = Analysis(**analysis_json)
    annotation_service = AnnotationService(collections['annotation'])
    annotation_service.queue_annotation_tasks(
        analysis, annotation_task_queue)
    background_tasks.add_task(
        AnnotationService.process_tasks, annotation_task_queue)

    return {"name": f"{name} annotations queued."}