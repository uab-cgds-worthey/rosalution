""" Analysis endpoint routes that serve up information regarding anaysis cases for rosalution """
import json

from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException, File

from ..core.phenotips_importer import PhenotipsImporter
from ..dependencies import database
from ..models.analysis import Analysis, AnalysisSummary
from ..models.phenotips_json import BasePhenotips

# This is temporarily changed as security is removed for the analysis endpoints to make development easier
# Change line 18 to the following to enable security:
# dependencies=[Depends(database), Security(get_authorization, scopes=["write"])]
# and add the following dependencies at the top:
# from fastapi import Security
# from ..security.security import get_authorization
router = APIRouter(prefix="/analysis",
                   tags=["analysis"], dependencies=[Depends(database)])


@router.get("/", response_model=List[Analysis])
def get_all_analyses(rosalution_db=Depends(database)):
    """Returns every analysis available"""
    return rosalution_db["analysis"].all()


@router.get("/summary", response_model=List[AnalysisSummary])
def get_all_analyses_summaries(rosalution_db=Depends(database)):
    """Returns a summary of every analysis within the application"""
    return rosalution_db["analysis"].all_summaries()


@router.get("/{name}", response_model=Analysis)
def get_analysis_by_name(name: str, rosalution_db=Depends(database)):
    """Returns analysis case data by calling method to find case by it's name"""
    return rosalution_db["analysis"].find_by_name(name)


@router.post("/import", response_model=Analysis)
async def import_phenotips_json(phenotips_input: BasePhenotips, rosalution_db=Depends(database)):
    """Imports the phenotips.json file into the database"""
    phenotips_importer = PhenotipsImporter(
        rosalution_db["analysis"], rosalution_db["genomic_unit"])
    try:
        return phenotips_importer.import_phenotips_json(phenotips_input)
    except ValueError as exception:
        raise HTTPException(status_code=409) from exception


@router.put("/update/{name}")
def update_analysis(name: str, analysis_data_changes: dict, rosalution_db=Depends(database)):
    """Updates an existing analysis"""
    return rosalution_db["analysis"].update_analysis(name, analysis_data_changes)


@router.post("/import_file")
async def create_file(phenotips_file: Union[bytes, None] = File(default=None), rosalution_db=Depends(database)):
    """ Imports a .json file for a phenotips case """
    # Quick and dirty json loads
    phenotips_input = BasePhenotips(**json.loads(phenotips_file))

    phenotips_importer = PhenotipsImporter(rosalution_db["analysis"], rosalution_db["genomic_unit"])
    try:
        return phenotips_importer.import_phenotips_json(phenotips_input)
    except ValueError as exception:
        raise HTTPException(status_code=409) from exception
