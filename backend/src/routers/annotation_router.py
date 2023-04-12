""" Annotation endpoint routes that handle all things annotation within the application """

from datetime import date, datetime

from fastapi import (
    APIRouter, Depends, BackgroundTasks, HTTPException, status, UploadFile, File, Form, Response, Security
)

from ..enums import GenomicUnitType
from ..core.annotation import AnnotationService
from ..dependencies import database, annotation_queue
from ..models.analysis import Analysis

from ..security.security import get_current_user

router = APIRouter(
    prefix="/annotate",
    tags=["annotation"],
    dependencies=[Depends(database), Depends(annotation_queue),
                  Security(get_current_user)],
)


@router.post("/{name}", status_code=status.HTTP_202_ACCEPTED)
def annotate_analysis(
    name: str,
    background_tasks: BackgroundTasks,
    repositories=Depends(database),
    annotation_task_queue=Depends(annotation_queue),
):
    """
    Placeholder to initiate annotations for an analysis. This queueing/running
    annotations for a sample will be moved to the analysis creation endpoint
    when it is created in an upcomming update.
    """
    analysis_json = repositories["analysis"].find_by_name(name)
    if analysis_json is None:
        raise HTTPException(status_code=404, detail=f"'{name}' Analysis not found.")

    analysis = Analysis(**analysis_json)
    annotation_service = AnnotationService(repositories["annotation_config"])
    annotation_service.queue_annotation_tasks(analysis, annotation_task_queue)
    background_tasks.add_task(AnnotationService.process_tasks, annotation_task_queue, repositories['genomic_unit'])

    return {"name": f"{name} annotations queued."}


@router.get("/gene/{gene}")
def get_annotations_by_gene(gene, repositories=Depends(database)):
    """Returns annotations data by calling method to find annotations by gene"""

    genomic_unit = {
        'type': GenomicUnitType.GENE,
        'unit': gene,
    }

    queried_genomic_unit = repositories["genomic_unit"].find_genomic_unit(genomic_unit)

    if queried_genomic_unit is None:
        raise HTTPException(status_code=404, detail="Item not found")

    annotations = {}
    for annotation in queried_genomic_unit['annotations']:
        for dataset in annotation:
            if len(annotation[dataset]) > 0:
                annotations[dataset] = annotation[dataset][0]['value']

    return annotations


@router.get("/hgvsVariant/{variant}")
def get_annotations_by_hgvs_variant(variant: str, repositories=Depends(database)):
    """Returns annotations data by calling method to find annotations for variant and relevant transcripts
    by HGVS Variant"""

    genomic_unit = {
        'type': GenomicUnitType.HGVS_VARIANT,
        'unit': variant,
    }

    queried_genomic_unit = repositories["genomic_unit"].find_genomic_unit(genomic_unit)

    if queried_genomic_unit is None:
        raise HTTPException(status_code=404, detail="Item not found")

    annotations = {}
    for annotation in queried_genomic_unit['annotations']:
        for dataset in annotation:
            if len(annotation[dataset]) > 0:
                annotations[dataset] = annotation[dataset][0]['value']

    transcript_annotation_list = []
    for transcript_annotation in queried_genomic_unit['transcripts']:
        queried_transcript_annotation = {}
        for annotation in transcript_annotation['annotations']:
            for dataset in annotation:
                if len(annotation[dataset]) > 0:
                    queried_transcript_annotation[dataset] = annotation[dataset][0]['value']
        transcript_annotation_list.append(queried_transcript_annotation)

    return {**annotations, "transcripts": transcript_annotation_list}


@router.post("/{genomic_unit}/attach/image")
def upload_annotation_section(
    response: Response,
    genomic_unit: str,
    genomic_unit_type: GenomicUnitType = Form(...),
    section_name: str = Form(...),
    upload_file: UploadFile = File(...),
    repositories=Depends(database)
):
    """ This endpoint specifically handles annotation section image uploads """
    try:
        new_file_object_id = repositories["bucket"].save_file(
            upload_file.file, upload_file.filename, upload_file.content_type
        )
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    genomic_unit = {
        'unit': genomic_unit,
        'type': genomic_unit_type,
    }

    annotation_unit = {
        "data_set": section_name,
        "data_source": "rosalution-manual",
        "version": str(date.today()),
        "value": {"file_id": str(new_file_object_id), "created_date": str(datetime.now())},
    }

    try:
        repositories['genomic_unit'].annotate_genomic_unit_with_file(genomic_unit, annotation_unit)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    response.status_code = status.HTTP_201_CREATED

    return {'section': section_name, 'image_id': str(new_file_object_id)}


@router.post("/{genomic_unit}/update/image/{file_id}")
def update_annotation_image(
    file_id: str,
    genomic_unit: str,
    genomic_unit_type: GenomicUnitType = Form(...),
    section_name: str = Form(...),
    upload_file: UploadFile = File(...),
    repositories=Depends(database)
):
    """ Updates and replaces an annotation image with a new image  """

    try:
        new_file_id = repositories["bucket"].save_file(upload_file.file, upload_file.filename, upload_file.content_type)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    genomic_unit = {'unit': genomic_unit, 'type': genomic_unit_type}
    annotation_value = {"file_id": str(new_file_id), "created_date": str(datetime.now())}

    try:
        repositories['genomic_unit'].update_genomic_unit_file_annotation(
            genomic_unit, annotation_value, section_name, file_id
        )
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    try:
        repositories["genomic_unit"].remove_genomic_unit_file_annotation(genomic_unit, section_name, file_id)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    try:
        repositories["bucket"].delete_file(file_id)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    return {'section': section_name, 'image_id': str(new_file_id)}


@router.delete("/{genomic_unit}/remove/image/{file_id}")
def remove_annotation_image(
    genomic_unit: str,
    file_id: str,
    genomic_unit_type: GenomicUnitType = Form(...),
    section_name: str = Form(...),
    repositories=Depends(database)
):
    """ This endpoint handles removing an annotation image for specified genomic unit """
    genomic_unit = {'unit': genomic_unit, 'type': genomic_unit_type}

    try:
        repositories["genomic_unit"].remove_genomic_unit_file_annotation(genomic_unit, section_name, file_id)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    try:
        return repositories["bucket"].delete_file(file_id)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception
