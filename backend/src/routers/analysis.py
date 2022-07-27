""" Analysis endpoint routes that serve up information regarding anaysis cases for rosalution """

from typing import List

from fastapi import APIRouter, Depends

from ..core.analysis import Analysis, AnalysisSummary
from ..dependencies import database

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
