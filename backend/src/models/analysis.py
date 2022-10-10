"""
Manages Analyses for rosalution. An analysis within rosalution comprises of
of identifiers, case notes, and the genomic units being analyzed.
"""
# pylint: disable=too-few-public-methods
from datetime import date
from typing import List, Optional
from pydantic import BaseModel

from ..enums import GenomicUnitType


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
                    units.append(
                        {
                            "unit": variant["hgvs_variant"],
                            "type": GenomicUnitType.HGVS_VARIANT,
                            "genomic_build": variant["build"],
                            "transcript": variant["hgvs_variant"].split(':')[0]
                        }
                    )

        return units
