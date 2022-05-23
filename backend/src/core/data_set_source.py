"""
Models Data Sets that are used to annotate genomic units.
"""
# pylint: disable=too-few-public-methods
from typing import Optional
from pydantic import BaseModel

from ..enums import GenomicUnitType
from ..enums import AnnotationSourceType


class DataSetSource(BaseModel):
    """An annotation source that matches a data set with the type of data it is used to annotate and its source"""
    genomic_unit_type: GenomicUnitType
    data_set: str
    data_source: str
    url: Optional[str]
    annotation_source_type: AnnotationSourceType
    query_param: Optional[str]
    attribute: Optional[str]
