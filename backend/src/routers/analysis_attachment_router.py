"""Analysis endpoints for adding/updating/removing document and link attachments to an analysis."""

import json
from typing import Annotated, List
from fastapi import APIRouter, Depends, File, Form, HTTPException, Security, UploadFile
from pydantic import BaseModel, model_validator

from ..dependencies import database
from ..security.security import get_write_project_authorization

router = APIRouter(tags=["analysis attachments"])


class IncomingNewAttachment(BaseModel, frozen=True):
    """The sections of case notes associated with an analysis"""
    # Disabling duplicate warning, two incomming FormData is similar right now
    # but only in shorterm. We will come back and either revise the API schema
    # or abstract to the models module.
    #pylint disable=R0801
    name: str | None = None

    attachment_id: str | None = None
    comments: str | None = None
    link_name: str | None = None
    link: str | None = None
    data: str | None = None

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        """Allows FastAPI to valid and unpack the JSON of data into the model"""
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class IncommingUpdatedAttachment(BaseModel, frozen=True):
    """The sections of case notes associated with an analysis"""

    name: str | None = None

    attachment_id: str | None = None
    comments: str | None = None
    link_name: str | None = None
    link: str | None = None
    data: str | None = None


@router.post(
    "/{analysis_name}/attachment", response_model=List, dependencies=[Security(get_write_project_authorization)]
)
def attach_file(
    analysis_name: str,
    new_attachment: Annotated[IncomingNewAttachment, Form()],
    upload_file: UploadFile = File(None),
    repositories=Depends(database)
):
    """Uploads a file to GridFS and adds it to the analysis"""
    updated_analysis_json = None

    if new_attachment.link:
        updated_analysis_json = repositories["analysis"].attach_link(
            analysis_name, new_attachment.link_name, new_attachment.link, new_attachment.comments
        )
    else:
        new_file_object_id = repositories['bucket'].save_file(
            upload_file.file, upload_file.filename, upload_file.content_type
        )

        updated_analysis_json = repositories["analysis"].attach_file(
            analysis_name, new_file_object_id, upload_file.filename, new_attachment.comments
        )

    return updated_analysis_json["attachments"]


@router.put(
    "/{analysis_name}/attachment/{attachment_id}",
    response_model=List,
    dependencies=[Security(get_write_project_authorization)]
)
def update_attachment(
    analysis_name: str,
    attachment_id: str,
    updated_attachment: Annotated[IncommingUpdatedAttachment, Form()],
    repositories=Depends(database),
):
    """ Updates the attachment in the analysis """
    content = {
        'name': updated_attachment.name,
        'data': updated_attachment.data,
        'comments': updated_attachment.comments,
    }

    try:
        updated_analysis_json = repositories["analysis"].update_attachment(analysis_name, attachment_id, content)
        return updated_analysis_json["attachments"]
    except ValueError as exception:
        raise HTTPException(status_code=404, detail=str(exception)) from exception


@router.delete(
    "/{analysis_name}/attachment/{attachment_id}",
    response_model=List,
    dependencies=[Security(get_write_project_authorization)]
)
def remove_attachment(analysis_name: str, attachment_id: str, repositories=Depends(database)):
    """ Removes attachment from the analysis """
    if repositories["bucket"].id_exists(attachment_id):
        repositories["bucket"].delete_file(attachment_id)
    updated_analysis_json = repositories["analysis"].remove_attachment(analysis_name, attachment_id)
    return updated_analysis_json["attachments"]
