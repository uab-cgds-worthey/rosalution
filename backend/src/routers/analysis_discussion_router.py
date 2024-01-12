# pylint: disable=too-many-arguments
# Due to adding scope checks, it's adding too many arguments (7/6) to functions, so diabling this for now.
# Need to refactor later.
""" Analysis endpoint routes that provide an interface to interact with an Analysis' discussions """
from datetime import datetime, timezone
import logging
from uuid import uuid4

from fastapi import (APIRouter, Depends, Form, Security)

from ..dependencies import database
from ..models.user import VerifyUser
from ..security.security import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(tags=["analysis"], dependencies=[Depends(database)])


def mock_discussion_fixture():
    """Mock dicussion fixture to fake the discussions being returned"""
    return [{
        "post_id": "90jkflsd8d-6298-4afb-add5-6ef710eb5e98", "author_id": "3bghhsmnyqi6uxovazy07ryn9q1tqbnt",
        "author_fullname": "Hello Person", "publish_timestamp": "2023-10-09T21:13:22.687000",
        "content": "Nulla diam mi, semper vitae.", "attachments": [], "thread": []
    }, {
        "post_id": "a677fdsfsacf8-4ff9-a406-b113a7952f7e", "author_id": "kw0g790fdx715xsr1ead2jk0pqubtlyz",
        "author_fullname": "Developer Person", "publish_timestamp": "2023-10-10T21:13:22.687000",
        "content": "Morbi laoreet justo.", "attachments": [], "thread": []
    }, {
        "post_id": "e602ffdsfa-fdsfdsa-9f42-862c826255ef", "author_id": "exqkhvidr7uh2ndslsdymbzfbmqjlunk",
        "author_fullname": "Variant Review Report Preparer Person", "publish_timestamp": "2023-10-13T21:13:22.687000",
        "content": "Mauris pretium sem at nunc sollicitudin also.", "attachments": [], "thread": []
    }]


@router.get("/{analysis_name}/discussions")
def get_analysis_discussions(analysis_name: str):
    """ Returns a list of genomic units for a given analysis """
    logger.info("Retrieving the analysis '%s' discussions ", analysis_name)
    return mock_discussion_fixture()


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

    return repositories['analysis'].add_discussion_post(analysis_name, new_discussion_post)

@router.put("/{analysis_name}/discussions")
def update_analysis_discussion_post(
    analysis_name: str,
    discussion_post_id: str = Form(...),
    discussion_content: str = Form(...),
    repositories=Depends(database),
    client_id: VerifyUser = Security(get_current_user)
):
    logger.info("Editing post '%s' by user '%s' from the analysis '%s' with new content: '%s'", 
                discussion_post_id, client_id, analysis_name, discussion_content)

    return repositories['analysis'].updated_discussion_post(
        discussion_post_id, discussion_content, client_id, analysis_name
    )

@router.delete("/{analysis_name}/discussions")
def delete_analysis_discussion(
    analysis_name: str,
    discussion_post_id: str,
    repositories=Depends(database),
    client_id: VerifyUser = Security(get_current_user)
):
    logger.info("Deleting post %s by user '%s' from the analysis '%s'", discussion_post_id, client_id, analysis_name)

    return repositories['analysis'].delete_discussion_post(discussion_post_id, client_id, analysis_name)
