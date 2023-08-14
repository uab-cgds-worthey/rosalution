# pylint: disable=too-many-arguments
# Due to adding scope checks, it's adding too many arguments (7/6) to functions, so diabling this for now.
# Need to refactor later.
""" Analysis endpoint routes that serve up information regarding anaysis cases for rosalution """
import logging
import json

from typing import List, Optional, Union

from fastapi import (
    APIRouter, BackgroundTasks, Depends, HTTPException, File, status, UploadFile, Form, Response, Security
)
from fastapi.responses import StreamingResponse

from ..core.annotation import AnnotationService
from ..core.phenotips_importer import PhenotipsImporter
from ..dependencies import database, annotation_queue
from ..models.analysis import Analysis, AnalysisSummary
from ..models.event import Event
from ..enums import ThirdPartyLinkType
from ..models.phenotips_json import BasePhenotips
from ..models.user import VerifyUser
from ..security.security import get_authorization, get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analysis", tags=["analysis"], dependencies=[Depends(database)])


@router.get("/", response_model=List[Analysis])
def get_all_analyses(repositories=Depends(database)):
    """Returns every analysis available"""
    return repositories["analysis"].all()


@router.get("/summary", response_model=List[AnalysisSummary])
def get_all_analyses_summaries(repositories=Depends(database)):
    """Returns a summary of every analysis within the application"""
    return repositories["analysis"].all_summaries()


@router.get("/summary/{analysis_name}", response_model=AnalysisSummary)
def get_analysis_summary_by_name(analysis_name: str, repositories=Depends(database)):
    """Returns a summary of every analysis within the application"""
    return repositories["analysis"].summary_by_name(analysis_name)


@router.get("/{analysis_name}", response_model=Analysis, response_model_exclude_none=True)
def get_analysis_by_name(analysis_name: str, repositories=Depends(database)):
    """Returns analysis case data by calling method to find case by it's analysis_name"""
    return repositories["analysis"].find_by_name(analysis_name)


@router.get("/{analysis_name}/genomic_units")
def get_genomic_units(analysis_name: str, repositories=Depends(database)):
    """ Returns a list of genomic units for a given analysis """
    try:
        return repositories["analysis"].get_genomic_units(analysis_name)
    except ValueError as exception:
        raise HTTPException(status_code=404, detail=str(exception)) from exception


@router.post("/import_file", response_model=Analysis)
async def create_file(
    background_tasks: BackgroundTasks,
    phenotips_file: Union[bytes, None] = File(default=None),
    repositories=Depends(database),
    annotation_task_queue=Depends(annotation_queue),
    username: VerifyUser = Security(get_current_user),
    authorized=Security(get_authorization, scopes=["write"])
):
    """ Imports a .json file for a phenotips case """

    # Quick and dirty json loads
    phenotips_input = BasePhenotips(**json.loads(phenotips_file))

    phenotips_importer = PhenotipsImporter(repositories["analysis"], repositories["genomic_unit"])
    try:
        new_analysis = phenotips_importer.import_phenotips_json(phenotips_input.dict())
        new_analysis['timeline'].append(Event.timestamp_create_event(username).dict())
        repositories['analysis'].create_analysis(new_analysis)

    except ValueError as exception:
        raise HTTPException(status_code=409) from exception

    analysis = Analysis(**new_analysis)
    annotation_service = AnnotationService(repositories["annotation_config"])
    annotation_service.queue_annotation_tasks(analysis, annotation_task_queue)
    background_tasks.add_task(AnnotationService.process_tasks, annotation_task_queue, repositories['genomic_unit'])

    return new_analysis


@router.put("/{analysis_name}/mark_ready", response_model=Analysis)
def mark_ready(
    analysis_name: str,
    repositories=Depends(database),
    username: VerifyUser = Security(get_current_user),
    authorized=Security(get_authorization, scopes=["write"])
):
    """ Marks an analysis as ready for review """
    logger.info(authorized)
    try:
        return repositories["analysis"].mark_ready(analysis_name, username)
    except ValueError as exception:
        raise HTTPException(status_code=409, detail=str(exception)) from exception


@router.put("/{analysis_name}/update/sections", response_model=Analysis)
def update_analysis_sections(
    analysis_name: str,
    updated_sections: dict,
    repositories=Depends(database),
    authorized=Security(get_authorization, scopes=["write"])
):
    """Updates the sections that have changes"""
    logger.info(authorized)
    for (header, field) in updated_sections.items():
        for (updated_field, value) in field.items():
            if "Nominator" == updated_field:
                repositories["analysis"].update_analysis_nominator(analysis_name, '; '.join(value))
            repositories["analysis"].update_analysis_section(analysis_name, header, updated_field, {"value": value})

    return repositories["analysis"].find_by_name(analysis_name)


@router.get("/download/{file_id}")
def download_file_by_id(file_id: str, repositories=Depends(database)):
    """ Returns a file from GridFS using the file's id """
    grid_fs_file = repositories['bucket'].stream_analysis_file_by_id(file_id)
    return StreamingResponse(grid_fs_file, media_type=grid_fs_file.content_type)


@router.get("/{analysis_name}/download/{file_name}")
def download(analysis_name: str, file_name: str, repositories=Depends(database)):
    """ Returns a file saved to an analysis from GridFS by file name """
    # Does file exist by name in the given analysis?
    file = repositories['analysis'].find_file_by_name(analysis_name, file_name)

    if not file:
        raise HTTPException(status_code=404, detail="File not found.")

    return StreamingResponse(repositories['bucket'].stream_analysis_file_by_id(file['attachment_id']))


@router.post("/{analysis_name}/section/attach/image")
def attach_section_image(
    response: Response,
    analysis_name: str,
    upload_file: UploadFile = File(...),
    section_name: str = Form(...),
    field_name: str = Form(...),
    repositories=Depends(database),
    authorized=Security(get_authorization, scopes=["write"])
):
    """ Saves the uploaded image it to the specified field_name in the analysis's section."""

    logger.info(authorized)
    try:
        new_file_object_id = repositories["bucket"].save_file(
            upload_file.file, upload_file.filename, upload_file.content_type
        )
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    repositories["analysis"].add_section_image(analysis_name, section_name, field_name, new_file_object_id)

    response.status_code = status.HTTP_201_CREATED

    return {'section': section_name, 'field': field_name, 'image_id': str(new_file_object_id)}


@router.put("/{analysis_name}/section/update/{old_file_id}")
def update_analysis_section_image(
    analysis_name: str,
    old_file_id: str,
    upload_file: UploadFile = File(...),
    section_name: str = Form(...),
    field_name: str = Form(...),
    repositories=Depends(database),
    authorized=Security(get_authorization, scopes=["write"])
):
    """ Replaces the existing image by the file identifier with the uploaded one. """

    logger.info(authorized)
    # This needs try catch like in annotation router
    new_file_id = repositories["bucket"].save_file(upload_file.file, upload_file.filename, upload_file.content_type)

    repositories['analysis'].update_section_image(analysis_name, section_name, field_name, new_file_id, old_file_id)

    return {'section': section_name, 'field': field_name, 'image_id': str(new_file_id)}


@router.delete("/{analysis_name}/section/remove/{file_id}")
def remove_analysis_section_image(
    analysis_name: str,
    file_id: str,
    section_name: str = Form(...),
    field_name: str = Form(...),
    repositories=Depends(database),
    authorized=Security(get_authorization, scopes=["write"])
):
    """ Removes the image from an analysis section's field by its file_id """
    logger.info(authorized)
    try:
        repositories['analysis'].remove_analysis_section_file(analysis_name, section_name, field_name, file_id)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    try:
        return repositories["bucket"].delete_file(file_id)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception


@router.post("/{analysis_name}/attach/file")
def attach_supporting_evidence_file(
    analysis_name: str, upload_file: UploadFile = File(...), comments: str = Form(...), repositories=Depends(database)
):
    """Uploads a file to GridFS and adds it to the analysis"""
    if bool(repositories["analysis"].find_file_by_name(analysis_name, upload_file.filename)):
        raise HTTPException(status_code=409, detail="File with the same name already exists in the given analysis")

    new_file_object_id = repositories['bucket'].save_file(
        upload_file.file, upload_file.filename, upload_file.content_type
    )

    return repositories["analysis"].attach_supporting_evidence_file(
        analysis_name, new_file_object_id, upload_file.filename, comments
    )


@router.post("/{analysis_name}/attach/link")
def attach_supporting_evidence_link(
    analysis_name: str,
    link_name: str = Form(...),
    link: str = Form(...),
    comments: str = Form(...),
    repositories=Depends(database)
):
    """Uploads a file to GridFS and adds it to the analysis"""
    return repositories["analysis"].attach_supporting_evidence_link(analysis_name, link_name, link, comments)


@router.put("/{analysis_name}/attach/{third_party_enum}", response_model=Analysis)
def attach_third_party_link(
    analysis_name: str,
    third_party_enum: ThirdPartyLinkType,
    link: str = Form(...),
    repositories=Depends(database),
    authorized=Security(get_authorization, scopes=["write"])
):
    """ This endpoint attaches a third party link to an analysis. """
    logger.info(authorized)
    try:
        if not isinstance(third_party_enum, ThirdPartyLinkType):
            raise ValueError(f"Third party link type {third_party_enum} is not supported")
        return repositories["analysis"].attach_third_party_link(analysis_name, third_party_enum, link)
    except ValueError as exception:
        raise HTTPException(status_code=409, detail=f"Error attaching third party link: {exception}") from exception


@router.put("/{analysis_name}/attachment/{attachment_id}/update")
def update_supporting_evidence(
    analysis_name: str,
    attachment_id: str,
    name: str = Form(...),
    data: Optional[str] = Form(None),
    comments: str = Form(...),
    repositories=Depends(database)
):
    """ Updates a supporting evidence file in an analysis """
    content = {
        'name': name,
        'data': data,
        'comments': comments,
    }
    try:
        return repositories["analysis"].update_supporting_evidence(analysis_name, attachment_id, content)
    except ValueError as exception:
        raise HTTPException(status_code=404, detail=str(exception)) from exception


@router.delete("/{analysis_name}/attachment/{attachment_id}/remove")
def remove_supporting_evidence(
    analysis_name: str,
    attachment_id: str,
    repositories=Depends(database),
    authorized=Security(get_authorization, scopes=["write"])
):
    """ Removes a supporting evidence file from an analysis """
    logger.info(authorized)
    if repositories["bucket"].id_exists(attachment_id):
        repositories["bucket"].delete_file(attachment_id)
    return repositories["analysis"].remove_supporting_evidence(analysis_name, attachment_id)
