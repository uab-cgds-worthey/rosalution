"""
Manages Analyses for rosalution. An analysis within rosalution comprises of
of identifiers, case notes, and the genomic units being analyzed.
"""
# pylint: disable=too-few-public-methods
from datetime import date
from multiprocessing import Event
import re
from typing import List, Optional
from pydantic import BaseModel, root_validator

from .event import Event

from ..enums import EventType, StatusType, GenomicUnitType


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
    latest_status: Optional[StatusType]
    created_date: Optional[date]
    last_modified_date: Optional[date]
    timeline: List[Event] = []

    # The structure of the root_validator from pydantic requires the method to be setup this way even if there is no
    # self being used and no self argument
    @root_validator
    def compute_dates_and_status(cls, values): #pylint: disable=no-self-argument,no-self-use
        """Computes the dates and status of an analysis from a timeline"""
        if len(values['timeline']) == 0:
            return values

        last_event = sorted(values['timeline'], key=lambda event: event.timestamp, reverse=True)[0]
        values['last_modified_date'] = last_event.timestamp.date()
        values['created_date'] = next(
            (event.timestamp.date() for event in values['timeline'] if event.event == EventType.CREATE),
            None
        )
        values['latest_status'] = StatusType.from_event(last_event.event)
        return values


class AnalysisSummary(BaseAnalysis):
    """Models the summary of an analysis"""

    genomic_units: List = []

class Analysis(BaseAnalysis):
    """Models a detailed analysis"""

    genomic_units: List[GenomicUnit] = []
    sections: List[Section] = []
    supporting_evidence_files: List = []

    def units_to_annotate(self):
        """Returns the types of genomic units within the analysis"""
        units = []
        for unit in self.genomic_units:
            if hasattr(unit, "gene"):
                units.append({"unit": unit.gene, "type": GenomicUnitType.GENE})
            for transcript in unit.transcripts:
                units.append(
                    {
                        "unit": transcript["transcript"],
                        "type": GenomicUnitType.TRANSCRIPT,
                    }
                )
            for variant in unit.variants:
                if "hgvs_variant" in variant and variant["hgvs_variant"]:
                    transcript = variant["hgvs_variant"].split(':')[0]
                    transcript_without_version = re.sub(r'\..*', '', transcript )
                    units.append(
                        {
                            "unit": variant["hgvs_variant"],
                            "type": GenomicUnitType.HGVS_VARIANT,
                            "genomic_build": variant["build"],
                            "transcript": transcript_without_version
                        }
                    )

        return units
