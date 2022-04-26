"""
Manages Analyses for diverGen. An analysis within divergen comprises of
of identifiers, case notes, and the genomic units being analyzed.
"""
# pylint: disable=too-few-public-methods
from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class GenomicUnit(BaseModel):
    """The basic units within an analysis"""
    gene: Optional[str] = None
    transcripts: List = []
    variants: List = []


class Section(BaseModel):
    """The sections of case notes associated with an analysis"""
    header: str
    content: List = []


class BaseAnalysis(BaseModel):
    """The share parts of an analysis and it's summary"""
    name: str
    description: Optional[str]
    nominated_by: str
    latest_status: str
    created_date: date
    last_modified_date: date


class Analysis(BaseAnalysis):
    """Models a detailed analysis"""
    genomic_units: List[GenomicUnit] = []
    sections: List[Section] = []


class AnalysisSummary(BaseAnalysis):
    """Models the summary of an analysis"""
    genomic_units: List = []
