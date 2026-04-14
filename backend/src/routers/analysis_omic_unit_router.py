"""Analysis endpoints for adding/updating/removing genomic units to an analysis."""

# pylint: disable=duplicate-code

from fastapi import APIRouter, Depends, Security, BackgroundTasks
from pydantic import BaseModel

from ..dependencies import database, annotation_queue
from ..security.security import get_project_authorization, get_write_project_authorization

from ..models.analysis import Analysis
from ..core.phenotips_importer import PhenotipsImporter
from ..core.annotation import AnnotationService

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

@router.post("/{analysis_name}/genomic_unit", tags=["analysis genomic units"],dependencies=[Security(get_write_project_authorization)])
def add_genomic_units(
    background_tasks: BackgroundTasks,
    analysis_name: str,
    new_genomic_unit: IncomingGenomicUnit,
    repositories=Depends(database),
    annotation_task_queue=Depends(annotation_queue)
):
    """Adding a new genomic unit to an analysis by Analysis Name"""

    new_genomic_unit_dict = new_genomic_unit.model_dump()


    updated_analysis_json = repositories["analysis"].add_genomic_units(analysis_name, new_genomic_unit_dict)

    # Annotating the new genomic unit added in the updated_analysis_json
    new_genomic_unit_dict["reference_genome"] = "GRCh38"

    new_genomic_unit_data = PhenotipsImporter.import_genomic_unit_collection_data(new_genomic_unit_dict, "gene")
    repositories["genomic_unit"].create_genomic_unit(new_genomic_unit_data)

    new_genomic_unit_data = PhenotipsImporter.import_genomic_unit_collection_data(new_genomic_unit_dict, "hgvs")
    repositories["genomic_unit"].create_genomic_unit(new_genomic_unit_data)

    # structuring list for units to annotate
    analysis = Analysis(**updated_analysis_json)
    new_genomic_units_list = []
    for unit in analysis.genomic_units:
        if unit.gene == new_genomic_unit_dict['gene']:
            new_genomic_units_list.append(unit)
            break

    # Getting units to annotate
    new_genomic_unit_to_annotate = analysis.units_to_annotate(new_genomic_units_list)

    # Calling AnnotationService to queue annotation tasks by given unit
    annotation_service = AnnotationService(repositories["annotation_config"])
    annotation_service.queue_annotation_tasks_by_unit(analysis, new_genomic_unit_to_annotate, annotation_task_queue)
    background_tasks.add_task(
        AnnotationService.process_tasks, annotation_task_queue, repositories['genomic_unit'], repositories["analysis"]
    )

    return updated_analysis_json["genomic_units"]

@router.put("/{analysis_name}/genomic_unit/{gene}/{hgvs_variant}",dependencies=[Security(get_write_project_authorization)])
def edit_genomic_unit_reason_of_interest(analysis_name: str, gene: str, hgvs_variant: str, edit_unit: IncomingEditGenomicUnit, repositories=Depends(database)):
    
    updated_analysis_json = repositories["analysis"].edit_genomic_unit_reason_of_interest(analysis_name, gene, hgvs_variant, edit_unit.reason_of_interest)

    return updated_analysis_json["genomic_units"]
