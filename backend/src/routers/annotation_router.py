""" Annotation endpoint routes that handle all things annotation within the application """
import logging

from datetime import date, datetime
from typing import List

from fastapi import (APIRouter, Depends, BackgroundTasks, HTTPException, status, UploadFile, File, Response, Security)

from ..enums import GenomicUnitType
from ..core.annotation import AnnotationService
from ..dependencies import database, annotation_queue
from ..models.analysis import Analysis

from ..security.security import get_authorization, get_write_project_authorization

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/annotation", tags=["annotation"])


@router.post(
    "/{analysis_name}", status_code=status.HTTP_202_ACCEPTED, dependencies=[Security(get_write_project_authorization)]
)
def annotate_analysis(
    analysis_name: str,
    background_tasks: BackgroundTasks,
    repositories=Depends(database),
    annotation_task_queue=Depends(annotation_queue)
):
    """
    Placeholder to initiate annotations for an analysis. This queueing/running
    annotations for a sample will be moved to the analysis creation endpoint
    when it is created in an upcomming update.
    """
    analysis_json = repositories["analysis"].find_by_name(analysis_name)
    if analysis_json is None:
        raise HTTPException(status_code=404, detail=f"'{analysis_name}' Analysis not found.")

    analysis = Analysis(**analysis_json)
    annotation_service = AnnotationService(repositories["annotation_config"])
    annotation_service.queue_annotation_tasks(analysis, annotation_task_queue)
    background_tasks.add_task(
        AnnotationService.process_tasks, annotation_task_queue, repositories['genomic_unit'], repositories["analysis"]
    )

    return {"name": f"{analysis_name} annotations queued."}


@router.post(
    "/{genomic_unit}/{data_set_name}/attachment",
    response_model=List,
    dependencies=[Security(get_authorization, scopes=["write"])]
)
def upload_annotation_section(
    response: Response,
    genomic_unit: str,
    data_set_name: str,
    genomic_unit_type: GenomicUnitType,
    upload_file: UploadFile = File(...),
    repositories=Depends(database)
):
    """ This endpoint specifically handles annotation section image uploads """

    if genomic_unit_type.INVALID == genomic_unit_type:
        raise HTTPException(status_code=404, detail="Invalid Genomic Unit Type")

    try:
        new_file_object_id = repositories["bucket"].save_file(
            upload_file.file, upload_file.filename, upload_file.content_type
        )
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    genomic_unit_json = {
        'unit': genomic_unit,
        'type': genomic_unit_type,
    }

    annotation_unit = {
        "data_set": data_set_name,
        "data_source": "rosalution-manual",
        "version": str(date.today()),
        "value": {"file_id": str(new_file_object_id), "created_date": str(datetime.now())},
    }

    try:
        updated_genomic_unit = repositories['genomic_unit'].annotate_genomic_unit_with_file(
            genomic_unit_json, annotation_unit
        )
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    response.status_code = status.HTTP_201_CREATED

    updated_annotation = next(
        (annotation for annotation in updated_genomic_unit['annotations'] if data_set_name in annotation), None
    )

    return updated_annotation[data_set_name][0]['value']


@router.put(
    "/{genomic_unit}/{data_set_name}/attachment/{old_file_id}",
    response_model=List,
    dependencies=[Security(get_authorization, scopes=["write"])]
)
def update_annotation_image(
    genomic_unit: str,
    data_set_name: str,
    old_file_id: str,
    genomic_unit_type: GenomicUnitType,
    upload_file: UploadFile = File(...),
    repositories=Depends(database)
):
    """ Updates and replaces an annotation image with a new image  """
    try:
        new_file_id = repositories["bucket"].save_file(upload_file.file, upload_file.filename, upload_file.content_type)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    genomic_unit_json = {'unit': genomic_unit, 'type': genomic_unit_type}
    annotation_value = {"file_id": str(new_file_id), "created_date": str(datetime.now())}

    try:
        repositories['genomic_unit'].update_genomic_unit_file_annotation(
            genomic_unit_json, data_set_name, annotation_value, old_file_id
        )
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    try:
        updated_genomic_unit = repositories["genomic_unit"].remove_genomic_unit_file_annotation(
            genomic_unit_json, data_set_name, old_file_id
        )
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    try:
        repositories["bucket"].delete_file(old_file_id)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    updated_annotation = next(
        (annotation for annotation in updated_genomic_unit['annotations'] if data_set_name in annotation), None
    )

    return updated_annotation[data_set_name][0]['value']


@router.delete(
    "/{genomic_unit}/{data_set_name}/attachment/{file_id}",
    response_model=List,
    dependencies=[Security(get_authorization, scopes=["write"])]
)
def remove_annotation_image(
    genomic_unit: str,
    data_set_name: str,
    file_id: str,
    genomic_unit_type: GenomicUnitType,
    repositories=Depends(database)
):
    """ This endpoint handles removing an annotation image for specified genomic unit """
    genomic_unit_json = {'unit': genomic_unit, 'type': genomic_unit_type}

    try:
        updated_genomic_unit = repositories["genomic_unit"].remove_genomic_unit_file_annotation(
            genomic_unit_json, data_set_name, file_id
        )
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    try:
        repositories["bucket"].delete_file(file_id)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    updated_annotation = next(
        (annotation for annotation in updated_genomic_unit['annotations'] if data_set_name in annotation), None
    )

    return updated_annotation[data_set_name][0]['value']
