"""
Manages Phenotips import for rosalution. A Phenotips json import within rosalution comprises of
an external ID, variants, and genes.
"""
# pylint: disable=too-few-public-methods
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class PhenotipsVariants(BaseModel):
    """Models a variant within a Phenotips json import"""
    model_config = ConfigDict(extra='ignore')

    gene: Optional[str] = None
    inheritance: Optional[str] = None
    zygosity: Optional[str] = None
    interpretation: Optional[str] = None
    transcript: Optional[str] = None
    protein: Optional[str] = None
    cdna: Optional[str] = None
    reference_genome: str


class PhenotipsGene(BaseModel):
    """Models a gene within a Phenotips json genes"""
    model_config = ConfigDict(extra='ignore')

    comments: Optional[str] = None
    gene: str
    id: Optional[str] = None
    strategy: Optional[list] = None
    status: Optional[str] = None


class PhenotipsHpoTerm(BaseModel):
    """Models a gene within a Phenotips json genes"""
    model_config = ConfigDict(extra='ignore')

    id: str
    label: str = ""


class BasePhenotips(BaseModel):
    """The share parts of a phenotips and it's summary"""
    model_config = ConfigDict(extra='ignore')

    date: datetime
    external_id: str
    variants: List[PhenotipsVariants] = []
    genes: List[PhenotipsGene] = []
    features: List[PhenotipsHpoTerm] = []
