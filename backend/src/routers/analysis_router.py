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
from ..models.analysis import Analysis, AnalysisSummary, Section
from ..models.event import Event
from ..enums import SectionRowType, ThirdPartyLinkType, EventType
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


@router.post("/", response_model=Analysis)
async def create_file(
    background_tasks: BackgroundTasks,
    phenotips_file: Union[bytes, None] = File(default=None),
    repositories=Depends(database),
    annotation_task_queue=Depends(annotation_queue),
    username: VerifyUser = Security(get_current_user),
    authorized=Security(get_authorization, scopes=["write"])  #pylint: disable=unused-argument
):
    """ Imports a .json file for a phenotips case """

    # Quick and dirty json loads
    phenotips_input = BasePhenotips(**json.loads(phenotips_file))

    phenotips_importer = PhenotipsImporter(repositories["analysis"], repositories["genomic_unit"])
    try:
        new_analysis = phenotips_importer.import_phenotips_json(phenotips_input.model_dump())
        new_analysis['timeline'].append(Event.timestamp_create_event(username).model_dump())
        repositories['analysis'].create_analysis(new_analysis)

    except ValueError as exception:
        raise HTTPException(status_code=409) from exception

    analysis = Analysis(**new_analysis)
    annotation_service = AnnotationService(repositories["annotation_config"])
    annotation_service.queue_annotation_tasks(analysis, annotation_task_queue)
    background_tasks.add_task(AnnotationService.process_tasks, annotation_task_queue, repositories['genomic_unit'])

    return new_analysis


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


@router.get("/{analysis_name}/summary", response_model=AnalysisSummary)
def get_analysis_summary_by_name(analysis_name: str, repositories=Depends(database)):
    """Returns a summary of every analysis within the application"""
    return repositories["analysis"].summary_by_name(analysis_name)


@router.put("/{analysis_name}/event/{event_type}", response_model=Analysis)
def update_event(
    analysis_name: str,
    event_type: EventType,
    repositories=Depends(database),
    username: VerifyUser = Security(get_current_user),
    authorized=Security(get_authorization, scopes=["write"]),  #pylint: disable=unused-argument
):
    """ Updates analysis status """

    try:
        return repositories["analysis"].update_event(analysis_name, username, event_type)
    except ValueError as exception:
        raise HTTPException(status_code=409, detail=str(exception)) from exception


@router.post("/{analysis_name}/sections", response_model=List[Section])
def update_analysis_sections(
    analysis_name: str,
    row_type: SectionRowType,
    updated_sections: List[Section],
    repositories=Depends(database),
    authorized=Security(get_authorization, scopes=["write"])  #pylint: disable=unused-argument
):
    """Updates the sections that have changes"""
    if row_type == SectionRowType.TEXT:
        update_analysis_sections_text_fields(analysis_name, updated_sections, repositories["analysis"])
        updated_analysis = repositories["analysis"].find_by_name(analysis_name)
        updated_analysis_model = Analysis(**updated_analysis)
        return updated_analysis_model.sections

    if row_type in (SectionRowType.IMAGE, SectionRowType.DOCUMENT):
        print("Will be adding image or document")

        if row_type == SectionRowType.DOCUMENT:
            print("Will be adding document")

        if row_type == SectionRowType.IMAGE:
            print("Will be adding image")

    if row_type == SectionRowType.LINK:
        print("will be adding link")

    print("ADDING TYPE NOT SUPPORTED YET, IN PROGRESS")
    return []


def update_analysis_sections_text_fields(analysis_name, updated_sections: List[Section], analysis_repository):
    """Updates each of the rows for each of the sections for the analysis within the analysis repository."""
    for section in updated_sections:
        for field in section.content:
            field_name, field_value = field["fieldName"], field["value"]
            if "Nominator" == field_name:
                analysis_repository.update_analysis_nominator(analysis_name, '; '.join(field_value))
            analysis_repository.update_analysis_section(
                analysis_name, section.header, field_name, {"value": field_value}
            )


@router.put("/{analysis_name}/section/attach/file")
def attach_animal_model_system_report(
    analysis_name: str,
    section_name: str = Form(...),
    field_name: str = Form(...),
    comments: str = Form(...),
    upload_file: UploadFile = File(...),
    repositories=Depends(database),
    authorized=Security(get_authorization, scopes=["write"])  #pylint: disable=unused-argument
):
    """ Attaches a file as supporting evidence to a section in an Analysis  """

    try:
        new_file_object_id = repositories["bucket"].save_file(
            upload_file.file, upload_file.filename, upload_file.content_type
        )
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    field_value_file = {
        "name": upload_file.filename, "attachment_id": str(new_file_object_id), "type": "file", "comments": comments
    }

    return repositories['analysis'].attach_section_supporting_evidence_file(
        analysis_name, section_name, field_name, field_value_file
    )


@router.put("/{analysis_name}/section/remove/file")
def remove_animal_model_system_report(
    analysis_name: str,
    section_name: str = Form(...),
    field_name: str = Form(...),
    attachment_id: str = Form(...),
    repositories=Depends(database),
    authorized=Security(get_authorization, scopes=["write"])  #pylint: disable=unused-argument
):
    """ Removes a supporting evidence file from an analysis section """

    if repositories["bucket"].id_exists(attachment_id):
        repositories["bucket"].delete_file(attachment_id)

    return repositories['analysis'].remove_section_supporting_evidence(analysis_name, section_name, field_name)


@router.put("/{analysis_name}/section/attach/link")
def attach_animal_model_system_imaging(
    analysis_name: str,
    section_name: str = Form(...),
    field_name: str = Form(...),
    link_name: str = Form(...),
    link: str = Form(...),
    comments: str = Form(...),
    repositories=Depends(database),
    authorized=Security(get_authorization, scopes=["write"])  #pylint: disable=unused-argument
):
    """ Attaches a link as supporting evidence to an analysis section """

    field_value_link = {"name": link_name, "data": link, "type": "link", "comments": comments}

    return repositories["analysis"].attach_section_supporting_evidence_link(
        analysis_name, section_name, field_name, field_value_link
    )


@router.put("/{analysis_name}/section/remove/link")
def remove_animal_model_system_imaging(
    analysis_name: str,
    section_name: str = Form(...),
    field_name: str = Form(...),
    repositories=Depends(database),
    authorized=Security(get_authorization, scopes=["write"])  #pylint: disable=unused-argument
):
    """ Removes a supporting evidence link from an analysis section """

    return repositories["analysis"].remove_section_supporting_evidence(analysis_name, section_name, field_name)


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
    authorized=Security(get_authorization, scopes=["write"])  #pylint: disable=unused-argument
):
    """ Saves the uploaded image it to the specified field_name in the analysis's section."""
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
    authorized=Security(get_authorization, scopes=["write"])  #pylint: disable=unused-argument
):
    """ Replaces the existing image by the file identifier with the uploaded one. """
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
    authorized=Security(get_authorization, scopes=["write"])  #pylint: disable=unused-argument
):
    """ Removes the image from an analysis section's field by its file_id """
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
    authorized=Security(get_authorization, scopes=["write"])  #pylint: disable=unused-argument
):
    """ This endpoint attaches a third party link to an analysis. """
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
    authorized=Security(get_authorization, scopes=["write"])  #pylint: disable=unused-argument
):
    """ Removes a supporting evidence file from an analysis """
    if repositories["bucket"].id_exists(attachment_id):
        repositories["bucket"].delete_file(attachment_id)
    return repositories["analysis"].remove_supporting_evidence(analysis_name, attachment_id)
