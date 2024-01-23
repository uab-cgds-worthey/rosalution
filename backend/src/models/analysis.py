"""
Manages Analyses for rosalution. An analysis within rosalution comprises of
of identifiers, case notes, and the genomic units being analyzed.
"""
# pylint: disable=too-few-public-methods
from datetime import date
import json
import re
from typing import List, Optional
from pydantic import BaseModel, computed_field, model_validator

from .event import Event

from ..enums import EventType, StatusType, GenomicUnitType


class GenomicUnit(BaseModel):
    """The basic units within an analysis"""

    gene: Optional[str] = None
    transcripts: List = []
    variants: List = []


class Section(BaseModel, frozen=True):
    """The sections of case notes associated with an analysis"""

    header: str
    attachment_field: Optional[str] = None
    content: List = []

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class BaseAnalysis(BaseModel):
    """The share parts of an analysis and it's summary"""

    name: str
    description: Optional[str] = None
    nominated_by: str
    timeline: List[Event] = []
    third_party_links: Optional[List] = []

    @computed_field
    @property
    def created_date(self) -> date:
        """The created date derived from the create event in the timeline"""
        if len(self.timeline) == 0:
            return None

        return next((event.timestamp.date() for event in self.timeline if event.event == EventType.CREATE), None)

    @computed_field
    @property
    def last_modified_date(self) -> date:
        """The last modified date derived from the last event in the timeline"""
        if len(self.timeline) == 0:
            return None

        last_event = sorted(self.timeline, key=lambda event: event.timestamp, reverse=True)[0]
        return last_event.timestamp.date()

    @computed_field
    @property
    def latest_status(self) -> StatusType:
        """The status as calculated from the events on the timeline"""
        if len(self.timeline) == 0:
            return None

        last_event = sorted(self.timeline, key=lambda event: event.timestamp, reverse=True)[0]
        return StatusType.from_event(last_event.event)


class AnalysisSummary(BaseAnalysis):
    """Models the summary of an analysis"""

    genomic_units: List[GenomicUnit] = []


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
                units.append({
                    "unit": transcript["transcript"],
                    "type": GenomicUnitType.TRANSCRIPT,
                })
            for variant in unit.variants:
                if "hgvs_variant" in variant and variant["hgvs_variant"]:
                    transcript = variant["hgvs_variant"].split(':')[0]
                    transcript_without_version = re.sub(r'\..*', '', transcript)
                    units.append({
                        "unit": variant["hgvs_variant"],
                        "type": GenomicUnitType.HGVS_VARIANT,
                        "genomic_build": variant["build"],
                        "transcript": transcript_without_version,
                    })

        return units
