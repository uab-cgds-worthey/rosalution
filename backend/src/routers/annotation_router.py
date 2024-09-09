# pylint: disable=too-many-arguments
# Due to adding scope checks, it's adding too many arguments (7/6) to functions, so diabling this for now.
# Need to refactor later.
""" Annotation endpoint routes that handle all things annotation within the application """
import logging

from datetime import date, datetime
from typing import List

from fastapi import (APIRouter, Depends, BackgroundTasks, HTTPException, status, UploadFile, File, Response, Security)

from ..enums import GenomicUnitType
from ..core.annotation import AnnotationService
from ..dependencies import database, annotation_queue
from ..models.analysis import Analysis

from ..security.security import get_authorization

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/annotation",
    tags=["annotation"],
    dependencies=[Depends(database), Depends(annotation_queue)],
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


@router.get("/gene/{gene}/analysis/{analysis_name}")
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


@router.get("/hgvsVariant/{variant}/analysis/{analysis_name}")
def get_annotations_by_hgvs_variant(variant: str, analysis_name: str, repositories=Depends(database)):
    """Returns annotations data by calling method to find annotations for variant and relevant transcripts
    by HGVS Variant"""

    genomic_unit = {
        'type': GenomicUnitType.HGVS_VARIANT,
        'unit': variant,
    }

    dataset_manifest = repositories["analyses"].get_dataset_manifest(analysis_name)
    queried_genomic_unit = repositories["genomic_unit"].find_genomic_unit(genomic_unit)

    if queried_genomic_unit is None:
        raise HTTPException(status_code=404, detail="Item not found")

    annotations = {}
    for annotation in queried_genomic_unit['annotations']:
        for dataset in annotation:
            dataset_config = next((config for config in dataset_manifest if dataset in config), None)
            if dataset_config is None:
                continue
            "annotation[dataset][0]['value']"
            found_dataset = next((by_version for by_version in annotation[dataset] if by_version in dataset_manifest), None)
            annotations[dataset] = 

    transcript_annotation_list = []
    for transcript_annotation in queried_genomic_unit['transcripts']:
        queried_transcript_annotation = {}
        for annotation in transcript_annotation['annotations']:
            for dataset in annotation:
                if len(annotation[dataset]) > 0:
                    queried_transcript_annotation[dataset] = annotation[dataset][0]['value']
        transcript_annotation_list.append(queried_transcript_annotation)

    return {**annotations, "transcripts": transcript_annotation_list}


@router.post("/{genomic_unit}/{data_set}/attachment", response_model=List)
def upload_annotation_section(
    response: Response,
    genomic_unit: str,
    data_set: str,
    genomic_unit_type: GenomicUnitType,
    upload_file: UploadFile = File(...),
    repositories=Depends(database),
    authorized=Security(get_authorization, scopes=["write"])  #pylint: disable=unused-argument
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
        "data_set": data_set,
        "data_source": "rosalution-manual",
        "version": str(date.today()),
        "value": {"file_id": str(new_file_object_id), "created_date": str(datetime.now())},
    }

    try:
        repositories['genomic_unit'].annotate_genomic_unit_with_file(genomic_unit_json, annotation_unit)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    response.status_code = status.HTTP_201_CREATED

    updated_annotation_value = repositories['genomic_unit'].find_genomic_unit_annotation_value(
        genomic_unit_json, data_set
    )

    return updated_annotation_value


@router.put("/{genomic_unit}/{data_set}/attachment/{old_file_id}", response_model=List)
def update_annotation_image(
    genomic_unit: str,
    data_set: str,
    old_file_id: str,
    genomic_unit_type: GenomicUnitType,
    upload_file: UploadFile = File(...),
    repositories=Depends(database),
    authorized=Security(get_authorization, scopes=["write"])  #pylint: disable=unused-argument
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
            genomic_unit_json, data_set, annotation_value, old_file_id
        )
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    try:
        repositories["genomic_unit"].remove_genomic_unit_file_annotation(genomic_unit_json, data_set, old_file_id)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    try:
        repositories["bucket"].delete_file(old_file_id)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    updated_annotation_value = repositories['genomic_unit'].find_genomic_unit_annotation_value(
        genomic_unit_json, data_set
    )

    return updated_annotation_value


@router.delete("/{genomic_unit}/{data_set}/attachment/{file_id}", response_model=List)
def remove_annotation_image(
    genomic_unit: str,
    data_set: str,
    file_id: str,
    genomic_unit_type: GenomicUnitType,
    repositories=Depends(database),
    authorized=Security(get_authorization, scopes=["write"])  #pylint: disable=unused-argument
):
    """ This endpoint handles removing an annotation image for specified genomic unit """
    genomic_unit_json = {'unit': genomic_unit, 'type': genomic_unit_type}

    try:
        repositories["genomic_unit"].remove_genomic_unit_file_annotation(genomic_unit_json, data_set, file_id)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    try:
        repositories["bucket"].delete_file(file_id)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    updated_annotation_value = repositories['genomic_unit'].find_genomic_unit_annotation_value(
        genomic_unit_json, data_set
    )

    return updated_annotation_value
