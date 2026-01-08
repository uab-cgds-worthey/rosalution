""" Analysis endpoint routes that serve up information regarding anaysis cases for rosalution """
import json

from typing import List, Union

from fastapi import (APIRouter, BackgroundTasks, Depends, HTTPException, File, Form, Security)
from fastapi.responses import StreamingResponse

from ..core.annotation import AnnotationService
from ..core.phenotips_importer import PhenotipsImporter
from ..dependencies import database, annotation_queue
from ..models.analysis import Analysis, AnalysisSummary
from ..models.event import Event
from ..enums import ThirdPartyLinkType, EventType
from ..models.phenotips_json import BasePhenotips
from ..models.user import VerifyUser
from ..security.security import get_authorization, get_current_user

from . import analysis_annotation_router
from . import analysis_attachment_router
from . import analysis_discussion_router
from . import analysis_section_router

router = APIRouter(prefix="/analysis", dependencies=[Depends(database)])
router.include_router(analysis_annotation_router.router)
router.include_router(analysis_attachment_router.router)
router.include_router(analysis_discussion_router.router)
router.include_router(analysis_section_router.router)


@router.get("", tags=["analysis"], response_model=List[Analysis])
def get_all_analyses(repositories=Depends(database), username: VerifyUser = Security(get_current_user)):  #pylint: disable=unused-argument
    """Returns every analysis available"""
    return repositories["analysis"].all()


@router.get("/summary", tags=["analysis"], response_model=List[AnalysisSummary])
async def get_all_analyses_summaries(repositories=Depends(database), client_id: VerifyUser = Security(get_current_user)):
    """Returns a summary of every analysis within the application"""
    return repositories["project"].all_summaries(client_id)


@router.post("", tags=["analysis"], response_model=Analysis)
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
    background_tasks.add_task(
        AnnotationService.process_tasks, annotation_task_queue, repositories['genomic_unit'], repositories["analysis"]
    )

    return new_analysis


@router.get("/{analysis_name}", tags=["analysis"], response_model=Analysis, response_model_exclude_none=True)
def get_analysis_by_name(
    analysis_name: str,
    repositories=Depends(database),
    username: VerifyUser = Security(get_current_user)  #pylint: disable=unused-argument
):
    """Returns analysis case data by calling method to find case by it's analysis_name"""
    analysis = repositories["analysis"].find_by_name(analysis_name)

    if analysis is None:
        raise HTTPException(status_code=404, detail=f"{analysis_name} does not exist.")
    return analysis


@router.get("/{analysis_name}/genomic_units", tags=["analysis"])
def get_genomic_units(analysis_name: str, repositories=Depends(database)):
    """ Returns a list of genomic units for a given analysis """
    try:
        return repositories["analysis"].get_genomic_units(analysis_name)
    except ValueError as exception:
        raise HTTPException(status_code=404, detail=str(exception)) from exception


@router.get("/{analysis_name}/summary", tags=["analysis"], response_model=AnalysisSummary)
def get_analysis_summary_by_name(analysis_name: str, repositories=Depends(database)):
    """Returns a summary of every analysis within the application"""
    return repositories["analysis"].summary_by_name(analysis_name)


@router.put("/{analysis_name}/event/{event_type}", tags=["analysis"], response_model=Analysis)
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


@router.get("/download/{file_id}", tags=["analysis"])
def download_file_by_id(
    file_id: str,
    repositories=Depends(database),
    username: VerifyUser = Security(get_current_user)  #pylint: disable=unused-argument
):
    """ Returns a file from GridFS using the file's id """
    grid_fs_file = repositories['bucket'].stream_analysis_file_by_id(file_id)
    return StreamingResponse(grid_fs_file, media_type=grid_fs_file.content_type)


@router.get("/{analysis_name}/download/{file_name}", tags=["analysis"])
def download(
    analysis_name: str,
    file_name: str,
    repositories=Depends(database),
    username: VerifyUser = Security(get_current_user)  #pylint: disable=unused-argument
):
    """ Returns a file saved to an analysis from GridFS by file name """
    # Does file exist by name in the given analysis?
    file = repositories['analysis'].find_file_by_name(analysis_name, file_name)

    if not file:
        raise HTTPException(status_code=404, detail="File not found.")

    return StreamingResponse(repositories['bucket'].stream_analysis_file_by_id(file['attachment_id']))


@router.put("/{analysis_name}/attach/{third_party_enum}", tags=["analysis"], response_model=Analysis)
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
