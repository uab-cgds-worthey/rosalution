"""
Manages Phenotips import for rosalution. A Phenotips json import within rosalution comprises of
an external ID, variants, and genes.
"""
# pylint: disable=too-few-public-methods
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Extra


class PhenotipsVariants(BaseModel):
    """Models a variant within a Phenotips json import"""

    gene: Optional[str] = None
    inheritance: Optional[str] = None
    zygosity: Optional[str] = None
    interpretation: Optional[str] = None
    transcript: Optional[str] = None
    protein: Optional[str] = None
    cdna: Optional[str] = None
    reference_genome: str

    class config:  # pylint: disable=invalid-name
        """Configures the pydantic model"""

        extra = Extra.allow


class PhenotipsGene(BaseModel):
    """Models a gene within a Phenotips json genes"""

    comments: Optional[str] = None
    gene: str
    id: Optional[str] = None
    strategy: Optional[list] = None
    status: Optional[str] = None

    class config:  # pylint: disable=invalid-name
        """Configures the pydantic model"""

        extra = Extra.allow


class PhenotipsHpoTerm(BaseModel):
    """Models a gene within a Phenotips json genes"""

    id: str
    label: str = ""

    class config:  # pylint: disable=invalid-name
        """Configures the pydantic model"""

        extra = Extra.allow


class BasePhenotips(BaseModel):
    """The share parts of a phenotips and it's summary"""

    date: datetime
    external_id: str
    variants: List[PhenotipsVariants] = []
    genes: List[PhenotipsGene] = []
    features: List[PhenotipsHpoTerm] = []

    class config:  # pylint: disable=invalid-name
        """Configures the pydantic model"""

        extra = Extra.allow
