""" Analysis endpoint routes that serve up information regarding anaysis cases for rosalution """

from typing import List

from fastapi import (APIRouter, Depends, HTTPException, Form, Security, status)
from fastapi.responses import StreamingResponse

from ..dependencies import database
from ..models.analysis import Analysis, AnalysisSummary
from ..enums import ThirdPartyLinkType, EventType

from ..models.user import ProjectUser, VerifyUser
from ..security.security import get_current_user, get_project_authorization, \
    get_write_project_authorization

from . import analysis_annotation_router
from . import analysis_attachment_router
from . import analysis_discussion_router
from . import analysis_section_router

router = APIRouter(prefix="/analysis")
router.include_router(analysis_annotation_router.router)
router.include_router(analysis_attachment_router.router)
router.include_router(analysis_discussion_router.router)
router.include_router(analysis_section_router.router)


@router.get("", tags=["analysis"], response_model=List[Analysis])
def get_all_analyses(repositories=Depends(database), client_id: VerifyUser = Security(get_current_user)):
    """Returns every analysis available for a user"""
    return repositories["project"].all_analyses(client_id)


@router.get("/summary", tags=["analysis"], response_model=List[AnalysisSummary])
async def get_all_analyses_summaries(
    repositories=Depends(database), client_id: VerifyUser = Security(get_current_user)
):
    """Returns a summary of every analysis within the application"""
    return repositories["project"].all_summaries(client_id)


@router.get("/{analysis_name}", tags=["analysis"], response_model=Analysis, response_model_exclude_none=True)
def get_analysis_by_name(
    analysis_name: str, repositories=Depends(database), client_id: VerifyUser = Security(get_current_user)
):
    """Returns analysis case data by calling method to find case by it's analysis_name"""
    current_user = repositories["user"].find_by_client_id(client_id)
    found_analysis = repositories["analysis"].find_by_name(analysis_name)

    if found_analysis is None:
        raise HTTPException(status_code=404, detail=f"{analysis_name} does not exist.")

    analysis = Analysis(**found_analysis)
    user = ProjectUser(**current_user)

    if not user.is_authorized(analysis.project_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not apart of project")

    return analysis


@router.get("/{analysis_name}/genomic_units", tags=["analysis"], dependencies=[Security(get_project_authorization)])
def get_genomic_units(analysis_name: str, repositories=Depends(database)):
    """ Returns a list of genomic units for a given analysis """
    try:
        return repositories["analysis"].get_genomic_units(analysis_name)
    except ValueError as exception:
        raise HTTPException(status_code=404, detail=str(exception)) from exception


@router.get(
    "/{analysis_name}/summary",
    tags=["analysis"],
    response_model=AnalysisSummary,
    dependencies=[Security(get_project_authorization)]
)
def get_analysis_summary_by_name(
    analysis_name: str,
    repositories=Depends(database),
):
    """Returns a summary of every analysis within the application"""

    return repositories["analysis"].summary_by_name(analysis_name)


@router.put(
    "/{analysis_name}/event/{event_type}",
    tags=["analysis"],
    response_model=Analysis,
    dependencies=[Security(get_write_project_authorization)]
)
def update_event(
    analysis_name: str,
    event_type: EventType,
    repositories=Depends(database),
    client_id: VerifyUser = Security(get_current_user)
):
    """ Updates analysis status """

    try:
        return repositories["analysis"].update_event(analysis_name, client_id, event_type)
    except ValueError as exception:
        raise HTTPException(status_code=409, detail=str(exception)) from exception


@router.get("/download/{file_id}", tags=["analysis"])
def download_file_by_id(file_id: str, repositories=Depends(database)):
    """ Returns a file from GridFS using the file's id """
    grid_fs_file = repositories['bucket'].stream_analysis_file_by_id(file_id)
    return StreamingResponse(grid_fs_file, media_type=grid_fs_file.content_type)


@router.get(
    "/{analysis_name}/download/{file_name}", tags=["analysis"], dependencies=[Security(get_project_authorization)]
)
def download(analysis_name: str, file_name: str, repositories=Depends(database)):
    """ Returns a file saved to an analysis from GridFS by file name """
    # Does file exist by name in the given analysis?
    file = repositories['analysis'].find_file_by_name(analysis_name, file_name)

    if not file:
        raise HTTPException(status_code=404, detail="File not found.")

    return StreamingResponse(repositories['bucket'].stream_analysis_file_by_id(file['attachment_id']))


@router.put(
    "/{analysis_name}/attach/{third_party_enum}",
    tags=["analysis"],
    response_model=Analysis,
    dependencies=[Security(get_write_project_authorization)]
)
def attach_third_party_link(
    analysis_name: str, third_party_enum: ThirdPartyLinkType, link: str = Form(...), repositories=Depends(database)
):
    """ This endpoint attaches a third party link to an analysis. """
    try:
        if not isinstance(third_party_enum, ThirdPartyLinkType):
            raise ValueError(f"Third party link type {third_party_enum} is not supported")
        return repositories["analysis"].attach_third_party_link(analysis_name, third_party_enum, link)
    except ValueError as exception:
        raise HTTPException(status_code=409, detail=f"Error attaching third party link: {exception}") from exception
