"""Analysis endpoints for adding/updating/removing genomic units to an analysis."""

import json
from typing import Annotated, List
from fastapi import APIRouter, Depends, File, Form, HTTPException, Security
from pydantic import BaseModel, model_validator

from ..dependencies import database
from ..security.security import get_authorization

from ..models.analysis import Analysis, AnalysisSummary

router = APIRouter(prefix="/analysis", tags=["analysis genomic units"], dependencies=[Depends(database)])

@router.post("/{analysis_name}/genomic_unit", tags=["analysis genomic units"], response_model=Analysis)
def add_genomic_units(
  analysis_name: str,
  genomic_unit: str=Form(...),
  repositories=Depends(database),
  authorized=Security(get_authorization, scopes=["write"])
):
  """Adding a new genomic unit to an analysis by Analysis Name"""

  print("Am I reaching the endpoint?")
  updated_analysis_json = None
  print("This is the incoming genomic unit")
  print(genomic_unit)

  updated_analysis_json = repositories["analysis"].add_genomic_units(analysis_name, genomic_unit)

  return "Not added yet"
