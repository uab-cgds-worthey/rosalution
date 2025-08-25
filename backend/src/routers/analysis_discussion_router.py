""" Analysis endpoint routes that provide an interface to interact with an Analysis' discussions """
from datetime import datetime, timezone
from uuid import uuid4

import json
from typing import Annotated
from pydantic import BaseModel, model_validator

from fastapi import (APIRouter, Depends, Form, Security, HTTPException, status, File, UploadFile)

from ..dependencies import database
from ..models.user import VerifyUser
from ..models.analysis import Analysis
from ..security.security import get_current_user

router = APIRouter(tags=["analysis discussions"], dependencies=[Depends(database)])


# Disabling duplicate warning, two incomming FormData is similar right now
# but only in shorterm. We will come back and either revise the API schema
# or abstract to the models module.
class RosalutionAttachment(BaseModel):
    """The sections of case notes associated with an analysis"""  #pylint disable=R0801
    name: str | None = None

    attachment_id: str | None = None
    comments: str | None = None
    link_name: str | None = None
    link: str | None = None
    data: str | None = None
    type: str | None = None

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        """Allows FastAPI to valid and unpack the JSON of data into the model"""
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class IncomingDiscussionFormData(BaseModel):
    """Handles incoming Form Data to FastAPI from Discussions, and handles Rosalution Attachments"""
    attachments: list[RosalutionAttachment] = []

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        """Allows FastAPI to valid and unpack the JSON of data into the model"""
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


@router.get("/{analysis_name}/discussions")
def get_analysis_discussions(
    analysis_name: str,
    repositories=Depends(database),
    username: VerifyUser = Security(get_current_user)  #pylint: disable=unused-argument
):
    """ Returns a list of discussion posts for a given analysis """

    found_analysis = repositories['analysis'].find_by_name(analysis_name)

    if not found_analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Analysis '{analysis_name}' does not exist.'"
        )

    analysis = Analysis(**found_analysis)

    return analysis.discussions


@router.post("/{analysis_name}/discussions")
async def add_analysis_discussion(
    analysis_name: str,
    discussion_content: Annotated[list[str], Form()],
    attachments: Annotated[IncomingDiscussionFormData, Form()],
    attachment_files: Annotated[list[UploadFile] | None,
                                File(description="Multiple files as File")] = None,
    repositories=Depends(database),
    client_id: VerifyUser = Security(get_current_user)
):
    """ Adds a new analysis discussion post """
    found_analysis = repositories['analysis'].find_by_name(analysis_name)

    if not found_analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Analysis '{analysis_name}' does not exist.'"
        )

    analysis = Analysis(**found_analysis)
    current_user = repositories["user"].find_by_client_id(client_id)

    attachments_as_json = []

    for attachment in attachments.attachments:
        if not attachment.attachment_id and attachment.type == 'link':
            attachment.attachment_id = str(uuid4())
        elif not attachment.attachment_id and attachment.type == 'file':
            file = next((item for item in attachment_files if item.filename == attachment.name), None)
            if not file:
                attachment_error = f"'{attachment.name}' file failed to upload."
                raise HTTPException(status_code=400, detail=attachment_error)
            new_file_object_id = repositories['bucket'].save_file(file.file, file.filename, file.content_type)
            attachment.attachment_id = str(new_file_object_id)

        attachments_as_json.append(attachment.model_dump(exclude_none=True))

    new_discussion_post = {
        "post_id": str(uuid4()),
        "author_id": client_id,
        "author_fullname": current_user["full_name"],
        "publish_timestamp": datetime.now(timezone.utc),
        "content": discussion_content,
        "attachments": attachments_as_json,
        "thread": [],
    }

    return repositories['analysis'].add_discussion_post(analysis.name, new_discussion_post)


@router.put("/{analysis_name}/discussions/{discussion_post_id}")
def update_analysis_discussion_post(
    analysis_name: str,
    discussion_post_id: str,
    discussion_content: list[str],
    repositories=Depends(database),
    client_id: VerifyUser = Security(get_current_user)
):
    """ Updates a discussion post's content in an analysis by the discussion post id """
    found_analysis = repositories['analysis'].find_by_name(analysis_name)

    if not found_analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis '{analysis_name}' does not exist. Unable to update discussion post.'"
        )

    analysis = Analysis(**found_analysis)

    try:
        valid_post = analysis.find_authored_discussion_post(discussion_post_id, client_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    if not valid_post:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User cannot update post they did not author."
        )

    return repositories['analysis'].updated_discussion_post(valid_post['post_id'], discussion_content, analysis.name)


@router.delete("/{analysis_name}/discussions/{discussion_post_id}")
def delete_analysis_discussion(
    analysis_name: str,
    discussion_post_id: str,
    repositories=Depends(database),
    client_id: VerifyUser = Security(get_current_user)
):
    """ Deletes a discussion post in an analysis by the discussion post id """
    found_analysis = repositories['analysis'].find_by_name(analysis_name)

    if not found_analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis '{analysis_name}' does not exist. Unable to delete discussion post.'"
        )

    analysis = Analysis(**found_analysis)

    try:
        valid_post = analysis.find_authored_discussion_post(discussion_post_id, client_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    if not valid_post:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User cannot delete post they did not author."
        )

    file_attachments = [attachment for attachment in valid_post['attachments'] if attachment['type'] == 'file']
    for attachment in file_attachments:
        attachment_id = attachment['attachment_id']
        if analysis.is_file_attached(attachment_id) and repositories["bucket"].id_exists(attachment_id):
            repositories["bucket"].delete_file(attachment_id)

    if len(valid_post['thread']) > 0:
        return repositories['analysis'].clear_discussion_post_content(valid_post['post_id'], analysis.name)

    return repositories['analysis'].delete_discussion_post(valid_post['post_id'], analysis.name)


@router.post("/{analysis_name}/discussions/{discussion_post_id}/thread/")
async def add_analysis_discussion_reply(    #pylint: disable=too-many-arguments, too-many-locals
    analysis_name: str,
    discussion_post_id: str,
    discussion_reply_content: list[str],
    reply_attachments: Annotated[IncomingDiscussionFormData, Form()],
    reply_attachment_files: Annotated[list[UploadFile] | None,
                                      File(description="Multiple files as File")] = None,
    repositories=Depends(database),
    client_id: VerifyUser = Security(get_current_user)
):
    """Adds a new reply to a discussion post"""
    found_analysis = repositories['analysis'].find_by_name(analysis_name)

    if not found_analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis '{analysis_name}' does not exist. Unable to update discussion post.'"
        )

    analysis = Analysis(**found_analysis)
    current_user = repositories["user"].find_by_client_id(client_id)

    reply_attachments_as_json = []

    for attachment in reply_attachments.attachments:
        if not attachment.attachment_id and attachment.type == 'link':
            attachment.attachment_id = str(uuid4())
        elif not attachment.attachment_id and attachment.type == 'file':
            file = next((item for item in reply_attachment_files if item.filename == attachment.name), None)
            if not file:
                attachment_error = f"'{attachment.name}' file failed to upload."
                raise HTTPException(status_code=400, detail=attachment_error)
            new_file_object_id = repositories['bucket'].save_file(file.file, file.filename, file.content_type)
            attachment.attachment_id = str(new_file_object_id)

        reply_attachments_as_json.append(attachment.model_dump(exclude_none=True))

    new_discussion_reply = {
        "reply_id": str(uuid4()),
        "author_id": client_id,
        "author_fullname": current_user["full_name"],
        "publish_timestamp": datetime.now(timezone.utc),
        "content": discussion_reply_content,
        "reply_attachments": reply_attachments_as_json,
    }

    return repositories['analysis'].add_discussion_reply(discussion_post_id, analysis.name, new_discussion_reply)


@router.post("/{analysis_name}/discussions/{discussion_post_id}/thread/{discussion_reply_id}")
async def edit_analysis_discussion_reply(
    analysis_name: str,
    discussion_post_id: str,
    discussion_reply_id: str,
    discussion_reply_content: list[str],
    repositories=Depends(database),
    client_id: VerifyUser = Security(get_current_user)
):
    """Edits a reply in a discussion post"""

    found_analysis = repositories['analysis'].find_by_name(analysis_name)

    if not found_analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis '{analysis_name}' does not exist. Unable to update discussion post.'"
        )

    analysis = Analysis(**found_analysis)

    try:
        valid_reply = analysis.find_authored_discussion_reply(discussion_post_id, discussion_reply_id, client_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    if not valid_reply:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User cannot update reply they did not author."
        )

    return repositories['analysis'].updated_discussion_reply(
        discussion_post_id, analysis.name, valid_reply['reply_id'], discussion_reply_content
    )


@router.delete("/{analysis_name}/discussions/{discussion_post_id}/thread/{discussion_reply_id}")
async def delete_analysis_discussion_reply(
    analysis_name: str,
    discussion_post_id: str,
    discussion_reply_id: str,
    repositories=Depends(database),
    client_id: VerifyUser = Security(get_current_user)
):
    """Deletes reply from a discussion post's thread"""

    found_analysis = repositories['analysis'].find_by_name(analysis_name)

    if not found_analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis '{analysis_name}' does not exist. Unable to delete discussion reply.'"
        )

    analysis = Analysis(**found_analysis)

    try:
        valid_reply = analysis.find_authored_discussion_reply(discussion_post_id, discussion_reply_id, client_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    if not valid_reply:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User cannot delete reply they did not author."
        )

    return repositories['analysis'].delete_discussion_reply(discussion_post_id, analysis.name, valid_reply['reply_id'])
