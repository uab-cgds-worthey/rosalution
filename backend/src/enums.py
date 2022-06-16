"""
Enumerations for the rosalution project.
"""
from enum import Enum


class GenomicUnitType(str, Enum):
    """Enumeration of the different types of genomic units that can be analyzed"""

    GENE = "gene"
    TRANSCRIPT = "transcript"
    VARIANT = "variant"
    HGVS_VARIANT = "hgvs_variant"
    INVALID = "invalid"


class AnnotationSourceType(str, Enum):
    """Enumeration of the different types of annotation sources in the configuration"""

    HTTP = "http"
    CSV = "csv"
    NONE = "none"
