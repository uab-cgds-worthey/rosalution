""" Analysis endpoint routes that serve up information regarding anaysis cases for diverGen """

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Security

from ..core.analysis import Analysis, AnalysisSummary
from ..dependencies import database

from ..security.security import get_authorization

router = APIRouter(
    prefix="/analysis",
    tags=["analysis"],
    dependencies=[Depends(database)]
)

@router.get('/test', response_model=List[Analysis], dependencies=[Security(get_authorization, scopes=["write"])])
def get_all_analyses_test(collections=Depends(database)):
    """ Returns every analysis available"""
    return collections['analysis'].all()

@router.get('/', response_model=List[Analysis])
def get_all_analyses(collections=Depends(database)):
    """ Returns every analysis available"""
    return collections['analysis'].all()

@router.get('/summary', response_model=List[AnalysisSummary])
def get_all_analyses_summaries(collections=Depends(database)):
    """ Returns a summary of every analysis within the application"""
    return collections['analysis'].all_summaries()

@router.get('/{name}', response_model=Analysis)
def get_analysis_by_name(name: str, collections=Depends(database)):
    """ Returns analysis case data by calling method to find case by it's name"""
    if name == 'CPAM0002':
        return collections['analysis'].find_by_name('CPAM0002')
    if name == 'CPAM0046':
        return collections['analysis'].find_by_name('CPAM0046')
    if name == 'CPAM0053':
        return collections['analysis'].find_by_name('CPAM0053')

    raise HTTPException(status_code=404, detail="Item not found")
