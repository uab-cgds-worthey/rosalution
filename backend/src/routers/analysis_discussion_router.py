# pylint: disable=too-many-arguments
# Due to adding scope checks, it's adding too many arguments (7/6) to functions, so diabling this for now.
# Need to refactor later.
""" Analysis endpoint routes that provide an interface to interact with an Analysis' discussions """
from datetime import datetime, timezone
import logging
from uuid import uuid4

from fastapi import (APIRouter, Depends, Form, Security, HTTPException, status)

from ..dependencies import database
from ..models.user import VerifyUser
from ..models.analysis import Analysis
from ..security.security import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(tags=["analysis"], dependencies=[Depends(database)])


@router.get("/{analysis_name}/discussions")
def get_analysis_discussions(analysis_name: str, repositories=Depends(database)):
    """ Returns a list of discussion posts for a given analysis """
    logger.info("Retrieving the analysis '%s' discussions ", analysis_name)

    found_analysis = repositories['analysis'].find_by_name(analysis_name)

    if not found_analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Analysis '{analysis_name}' does not exist.'"
        )

    analysis = Analysis(**found_analysis)

    return analysis.discussions


@router.post("/{analysis_name}/discussions")
def add_analysis_discussion(
    analysis_name: str,
    discussion_content: str = Form(...),
    repositories=Depends(database),
    client_id: VerifyUser = Security(get_current_user)
):
    """ Adds a new analysis topic """
    logger.info("Adding the analysis '%s' from user '%s'", analysis_name, client_id)
    logger.info("The message: %s", discussion_content)

    found_analysis = repositories['analysis'].find_by_name(analysis_name)

    if not found_analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Analysis '{analysis_name}' does not exist.'"
        )

    analysis = Analysis(**found_analysis)
    current_user = repositories["user"].find_by_client_id(client_id)

    new_discussion_post = {
        "post_id": str(uuid4()),
        "author_id": client_id,
        "author_fullname": current_user["full_name"],
        "publish_timestamp": datetime.now(timezone.utc),
        "content": discussion_content,
        "attachments": [],
        "thread": [],
    }

    return repositories['analysis'].add_discussion_post(analysis.name, new_discussion_post)


@router.put("/{analysis_name}/discussions/{discussion_post_id}")
def update_analysis_discussion_post(
    analysis_name: str,
    discussion_post_id: str,
    discussion_content: str = Form(...),
    repositories=Depends(database),
    client_id: VerifyUser = Security(get_current_user)
):
    """ Updates a discussion post's content in an analysis by the discussion post id """
    logger.info(
        "Editing post '%s' by user '%s' from the analysis '%s' with new content: '%s'", discussion_post_id, client_id,
        analysis_name, discussion_content
    )

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
    logger.info("Deleting post %s by user '%s' from the analysis '%s'", discussion_post_id, client_id, analysis_name)

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

    print(client_id)

    if not valid_post:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User cannot delete post they did not author."
        )

    return repositories['analysis'].delete_discussion_post(valid_post['post_id'], analysis.name)
