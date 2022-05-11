"""
Models annotation sources.
"""
# pylint: disable=too-few-public-methods
from pydantic import BaseModel

from ..enums import GenomicUnitType


class AnnotationSource(BaseModel):
    """An annotation source that matches a data set with the type of data it is used to annotate and its source"""
    type: GenomicUnitType
    data_set: str
    data_source: str
