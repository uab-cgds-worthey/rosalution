"""Analysis endpoints for adding/updating/removing genomic units to an analysis."""

import json
from fastapi import APIRouter, Depends, File, Form, Security
from pydantic import BaseModel, model_validator

from ..dependencies import database
from ..security.security import get_authorization

from ..core.phenotips_importer import PhenotipsImporter

router = APIRouter(tags=["analysis genomic units"])

class IncomingGenomicUnit(BaseModel):
  gene: str
  transcript: str | None = None
  cdna: str | None = None
  protein: str | None = None
  reason_of_interest: str

@router.post("/{analysis_name}/genomic_unit", tags=["analysis genomic units"])
def add_genomic_units(
  analysis_name: str,
  new_genomic_unit: IncomingGenomicUnit,
  repositories=Depends(database),
  # authorized=Security(get_authorization, scopes=["write"])
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

  return updated_analysis_json["genomic_units"]



# @router.post("/{analysis_name}/genomic_unit/annotate", tags=["analysis genomic units"])
# def annotate_added_genomic_units(
#   analysis_name: str,
#   new_genomic_unit: IncomingGenomicUnit,
#   repositories=Depends(database),
#   # authorized=Security(get_authorization, scopes=["write"])
# ):
#   """Annotating a newly added genomic unit to an analysis"""

#   new_genomic_unit_dict = new_genomic_unit.model_dump()

#   analysis_json = repositories["analysis"].find_by_name(analysis_name)

#   # Annotating the new genomic unit added in the updated_analysis_json
#   new_genomic_unit_dict["reference_genome"] = "GRCh38"

#   new_genomic_unit_data = PhenotipsImporter.import_genomic_unit_collection_data(new_genomic_unit_dict, "gene")
#   repositories["genomic_unit"].create_genomic_unit(new_genomic_unit_data)

#   new_genomic_unit_data = PhenotipsImporter.import_genomic_unit_collection_data(new_genomic_unit_dict, "hgvs")
#   repositories["genomic_unit"].create_genomic_unit(new_genomic_unit_data)

#   # Annotating the genomic unit once it's added into the genomic unit collection


#   return analysis_json["genomic_units"]


