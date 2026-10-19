"""Analysis endpoints for adding/updating/removing genomic units to an analysis."""

# pylint: disable=duplicate-code

import json
from typing import Annotated
from fastapi import APIRouter, Depends, Security, BackgroundTasks, HTTPException, status
from pydantic import BaseModel


from ..dependencies import DatabaseDepends, annotation_queue
from ..security.security import get_write_project_authorization

from ..models.analysis import Analysis
from ..core.phenotips_importer import PhenotipsImporter
from ..core.annotation import AnnotationService
from ..config import Settings, get_settings

router = APIRouter(tags=["analysis genomic units"])


class IncomingGenomicUnit(BaseModel):
    """The incoming genomic unit added to an analysis"""
    gene: str
    transcript: str | None = None
    cdna: str | None = None
    protein: str | None = None
    reason_of_interest: list[str]


class IncomingEditGenomicUnit(BaseModel):
    """Editing the reason of interest for a genomic unit"""
    reason_of_interest: list[str]


@router.post(
    "/{analysis_name}/genomic_unit",
    tags=["analysis genomic units"],
    dependencies=[Security(get_write_project_authorization)]
)
async def add_genomic_units(
    background_tasks: BackgroundTasks,
    analysis_name: str,
    new_genomic_unit: IncomingGenomicUnit,
    repositories: DatabaseDepends,
    settings: Annotated[Settings, Depends(get_settings)],
    annotation_task_queue=Depends(annotation_queue)
):
    """Adding a new genomic unit to an analysis by Analysis Name"""

    new_genomic_unit_dict = new_genomic_unit.model_dump()

    updated_analysis_json = await repositories["analysis"].add_genomic_units(analysis_name, new_genomic_unit_dict)

    # Default setting the reference build to Build 38 due to Rosalution only supporting build 38 at this time
    new_genomic_unit_dict["reference_genome"] = "GRCh38"

    new_genomic_unit_data = PhenotipsImporter.import_genomic_unit_collection_data(new_genomic_unit_dict, "gene")
    await repositories["genomic_unit"].create_genomic_unit(new_genomic_unit_data)

    new_genomic_unit_data = PhenotipsImporter.import_genomic_unit_collection_data(new_genomic_unit_dict, "hgvs")
    await repositories["genomic_unit"].create_genomic_unit(new_genomic_unit_data)

    analysis = Analysis(**updated_analysis_json)
    new_genomic_units_list = []
    for unit in analysis.genomic_units:
        if unit.gene == new_genomic_unit_dict['gene']:
            new_genomic_units_list.append(unit)
            break

    new_genomic_unit_to_annotate = analysis.units_to_annotate(new_genomic_units_list)

    # Calling AnnotationService to queue annotation tasks by given unit
    annotation_service = AnnotationService(repositories["annotation_config"])
    await annotation_service.queue_annotation_tasks_by_unit(analysis, new_genomic_unit_to_annotate, annotation_task_queue)
    
    background_tasks.add_task(AnnotationService.process_tasks, annotation_task_queue, settings)

    return updated_analysis_json["genomic_units"]


@router.put(
    "/{analysis_name}/genomic_unit/{gene}/{hgvs_variant}", dependencies=[Security(get_write_project_authorization)]
)
async def edit_genomic_unit_reason_of_interest(
    analysis_name: str, gene: str, hgvs_variant: str, edit_unit: IncomingEditGenomicUnit, repositories: DatabaseDepends
):
    """Editing the reason of interest for a manually added genomic unit in an analysis"""

    updated_analysis_json = await repositories["analysis"].edit_genomic_unit_reason_of_interest(
        analysis_name, gene, hgvs_variant, edit_unit.reason_of_interest
    )

    return updated_analysis_json["genomic_units"]


@router.delete(
    "/{analysis_name}/genomic_unit/{gene}/{hgvs_variant}", dependencies=[Security(get_write_project_authorization)]
)
async def delete_manual_genomic_unit(analysis_name: str, gene: str, hgvs_variant: str, repositories: DatabaseDepends):
    """
    Deleting a manually added genomic unit from an analysis. Returns an HTTP 405 Method Not Allowed if the 
    genomic unit is an original from the analysis creation.
    """

    try:
        updated_analysis_json = await repositories["analysis"].delete_manual_omic_unit(analysis_name, gene, hgvs_variant)
    except ValueError as exception:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=str(exception)) from exception

    return updated_analysis_json["genomic_units"]
