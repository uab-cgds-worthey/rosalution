"""Analysis endpoints for adding/updating/removing genomic units to an analysis."""

import json
from typing import Annotated, List
from fastapi import APIRouter, Depends, File, Form, HTTPException, Security
from pydantic import BaseModel, model_validator

from ..dependencies import database
from ..security.security import get_authorization

from ..models.analysis import Analysis, AnalysisSummary

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
  
  print("Am I reaching the endpoint?")
  print("This is the incoming genomic unit")
  print(new_genomic_unit)

  new_genomic_unit_dict = new_genomic_unit.model_dump()

  updated_analysis_json = repositories["analysis"].add_genomic_units(analysis_name, new_genomic_unit_dict)

  return updated_analysis_json["genomic_units"]
