""" Project endpoint routes that serve projects related operations in REST API"""

import json
from typing import Annotated, List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, File, Security
1
from ..core.annotation import AnnotationService
from ..core.phenotips_importer import PhenotipsImporter
from ..dependencies import DatabaseDepends, annotation_queue
from ..models.analysis import Analysis, Project
from ..models.event import Event
from ..models.phenotips_json import BasePhenotips

from ..security.security import get_current_user, get_create_project_authorization

router = APIRouter(prefix="/project", tags=["project"])


@router.get("", tags=["project"], response_model=List[Project])
async def get_projects(repositories: DatabaseDepends, client_id: Annotated[str, Security(get_current_user)]):
    """List all projects available to the authenticated user."""
    return await repositories["project"].all_projects(client_id)


@router.post("/{project_id}/analysis", response_model=Analysis)
async def create_analysis(
    project_id: str,
    phenotips_file: Annotated[bytes, File()],
    background_tasks: BackgroundTasks,
    repositories: DatabaseDepends,
    user_project: Annotated[str, Security(get_create_project_authorization)],
    annotation_task_queue=Depends(annotation_queue),
):
    """Create an analysis within a project from an uploaded JSON file and queue annotation tasks by genomic units."""

    client_id, project_name = user_project

    phenotips_input = BasePhenotips(**json.loads(phenotips_file))
    phenotips_importer = PhenotipsImporter(repositories["analysis"], repositories["genomic_unit"])

    try:
        new_analysis = await phenotips_importer.import_phenotips_json(phenotips_input.model_dump())
        new_analysis['timeline'].append(Event.timestamp_create_event(client_id).model_dump())
        await repositories['analysis'].create_analysis(project_id, project_name, new_analysis)

    except ValueError as exception:
        raise HTTPException(status_code=409) from exception

    analysis = Analysis(**new_analysis)
    annotation_service = AnnotationService(repositories["annotation_config"])
    await annotation_service.queue_annotation_tasks(analysis, annotation_task_queue)
    background_tasks.add_task(
        AnnotationService.process_tasks, annotation_task_queue, repositories['genomic_unit'], repositories["analysis"]
    )

    return new_analysis
