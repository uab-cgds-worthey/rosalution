"""Analysis endpoints for adding/updating/removing document and link attachments to an analysis."""

from typing import Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, Security, UploadFile

from ..dependencies import database
from ..security.security import get_authorization

router = APIRouter(tags=["analysis attachments"], dependencies=[Depends(database)])


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
